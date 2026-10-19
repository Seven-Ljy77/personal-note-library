from sqlalchemy import text

def register_and_login_userAB(client) -> dict[str , dict[str , str]] :
    payloadA = {
        "username" : "Alice",
        "password" : "123"
    }

    payloadB = {
        "username" : "Peter",
        "password" : "123"
    }

    response = client.post("/api/auth/register" , json=payloadA)
    assert response.status_code == 200
    response = client.post("/api/auth/register" , json=payloadB)
    assert response.status_code == 200

    response = client.post("/api/auth/login" , json=payloadA)
    assert response.status_code == 200

    tokenA = {
        "access_token" : response.json()["access_token"],
        "refresh_token" : response.json()["refresh_token"]
    }

    response = client.post("/api/auth/login" , json=payloadB)
    assert response.status_code == 200

    tokenB = {
        "access_token" : response.json()["access_token"],
        "refresh_token" : response.json()["refresh_token"]
    }

    token = {
        "tokenA" : tokenA,
        "tokenB" : tokenB
    }

    return token


def create_note(client , access_token) -> int :
    response = client.post("/api/notes" , headers={
        "Authorization" : f"Bearer {access_token}"
    } , json={
        "title" : "title",
        "content" : "content"
    })
    assert response.status_code == 204

    response = client.get("/api/notes" , headers={
        "Authorization" : f"Bearer {access_token}"
    })
    assert response.status_code == 200
    data = response.json()
    note_id = data[0]["id"]

    return note_id
    


def test_user_cannot_read_others_note(client) :

    token = register_and_login_userAB(client)
    note_id = create_note(client , token["tokenB"]["access_token"])


    response = client.get(f"/api/notes/{note_id}" , headers={
        "Authorization" : f"Bearer {token["tokenA"]["access_token"]}"
    })

    assert response.status_code == 403

    response = client.get(f"/api/notes/{note_id}" , headers={
        "Authorization" : f"Bearer {token["tokenB"]["access_token"]}"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "title"
    assert data["content"] == "content"


def test_user_cannot_update_others_note(client) :
    
    token = register_and_login_userAB(client)
    note_id = create_note(client , token["tokenB"]["access_token"])

    response = client.patch(f"/api/notes/{note_id}" , headers={
        "Authorization" : f"Bearer {token["tokenA"]["access_token"]}"
    } , 
    json={
        "title" : "A",
        "content" : "B"
    })

    assert response.status_code == 403

    response = client.get(f"/api/notes/{note_id}" , headers={
        "Authorization" : f"Bearer {token["tokenB"]["access_token"]}"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "title"
    assert data["content"] == "content"


def test_user_cannot_delete_others_note(client) :
    
    token = register_and_login_userAB(client)
    note_id = create_note(client , token["tokenB"]["access_token"])

    response = client.delete(f"/api/notes/{note_id}" , headers={
        "Authorization" : f"Bearer {token["tokenA"]["access_token"]}"
    })

    assert response.status_code == 403

    response = client.get(f"/api/notes/{note_id}" , headers={
        "Authorization" : f"Bearer {token["tokenB"]["access_token"]}" 
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "title"
    assert data["content"] == "content"


def test_user_cannot_pin_others_note(client, test_engine) :

    token = register_and_login_userAB(client)
    note_id = create_note(client , token["tokenB"]["access_token"])

    with test_engine.connect() as connection :
        is_pinned = connection.execute(
            text(f"SELECT is_pinned FROM notes WHERE id = {note_id}")
        ).scalar_one_or_none()

    assert is_pinned == False

    response = client.post(f"/api/notes/{note_id}" , headers={
        "Authorization" : f"Bearer {token["tokenA"]["access_token"]}"
    })

    assert response.status_code == 403

    with test_engine.connect() as connection :
        is_pinned = connection.execute(
            text(f"SELECT is_pinned FROM notes WHERE id = {note_id}")
        ).scalar_one_or_none()

    assert is_pinned == False