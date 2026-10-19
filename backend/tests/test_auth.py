from sqlalchemy import text

def test_register_successful(client , test_engine) :
    payload = {
        "username" : "Alice" ,
        "password" : "123123"
    }

    response = client.post("/api/auth/register" , json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "Alice"
    assert isinstance(data["id"] , int) and data["id"] > 0
    assert data["is_active"] == True
    assert "password" not in data
    assert "hashed_password" not in data

    with test_engine.connect() as connection :
        username = connection.execute(
            text(f"select username from users where id = {data["id"]}")
        ).scalar_one()

    assert username == payload["username"]


def test_register_duplicate_username(client , test_engine) :
    payload = {
        "username" : "Alice",
        "password" : "123123"
    }

    response = client.post("/api/auth/register" , json=payload)

    assert response.status_code == 200

    response = client.post("/api/auth/register" , json=payload)

    assert response.status_code == 409

    with test_engine.connect() as connection :
        user_num = connection.execute(
            text("select COUNT(*) from users")
        ).scalar_one()

    assert user_num == 1


def test_login_successful(client) :
    payload = {
        "username" : "Alice",
        "password" : "123123"
    }

    response = client.post("/api/auth/register" , json=payload)
    assert response.status_code == 200

    response = client.post("/api/auth/login" , json=payload)
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["access_token"], str) and data["access_token"]
    assert isinstance(data["refresh_token"], str) and data["refresh_token"]
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client) :
    payload = {
        "username" : "Alice",
        "password" : "123123"
    }

    payload_wrong1 = {
        "username" : "Alice",
        "password" : "123"
    }

    payload_wrong2 = {
        "username" : "A",
        "password" : "123"
    }

    response = client.post("/api/auth/register" , json=payload)
    assert response.status_code == 200

    response = client.post("/api/auth/login" , json=payload_wrong1)
    assert response.status_code == 401

    response = client.post("/api/auth/login" , json=payload_wrong2)
    assert response.status_code == 401


def test_get_me_without_token(client) :
    response = client.get("/api/users/me")

    assert response.status_code == 401
    assert response.headers["www-Authenticate"] == "Bearer"


def test_get_me_with_token(client) :
    payload = {
        "username" : "Alice",
        "password" : "123123"
    }

    response = client.post("/api/auth/register" , json=payload)
    assert response.status_code == 200

    registered_id = response.json()["id"]

    response = client.post("/api/auth/login" , json=payload)
    assert response.status_code == 200

    data = response.json()
    access_token = data["access_token"]

    response = client.get("/api/users/me" , headers={
        "Authorization" : f"Bearer {access_token}"
    })

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["id"] , int)
    assert data["id"] == registered_id
    assert data["username"] == payload["username"]
    assert data["is_active"] == True
    assert data["notes_num"] == 0


def test_refresh_token(client) :
    payload = {
        "username" : "Alice",
        "password" : "123123"
    }

    response = client.post("/api/auth/register" , json=payload)
    assert response.status_code == 200
    response = client.post("/api/auth/login" , json=payload)
    assert response.status_code == 200

    data = response.json()

    response = client.post("/api/auth/refresh" , json={
        "refresh_token" : data["refresh_token"]
    })

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["access_token"], str) and data["access_token"]
    assert data["token_type"] == "bearer"

    response = client.get("/api/users/me" , headers={
        "Authorization" : f"Bearer {data["access_token"]}"
    })

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == payload["username"]


def test_logout_revokes_refresh_token(client) :
    payload = {
        "username" : "Alice",
        "password" : "123123"
    }

    response = client.post("/api/auth/register" , json=payload)
    assert response.status_code == 200
    response = client.post("/api/auth/login" , json=payload)
    assert response.status_code == 200

    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    response = client.post("/api/auth/refresh" , json={
        "refresh_token" : data["refresh_token"]
    })

    assert response.status_code == 200

    response = client.post("/api/auth/logout" , headers={
        "Authorization" : f"Bearer {access_token}"
    } , json={
        "refresh_token" : refresh_token
    })

    assert response.status_code == 204

    response = client.post("/api/auth/refresh" , json={
        "refresh_token" : data["refresh_token"]
    })

    assert response.status_code == 401