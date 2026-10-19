def test_openapi(client) :
    response = client.get("/openapi.json")
    assert response.status_code == 200

    data = response.json()
    
    assert "/api/auth/register" in data["paths"]

def test_docs(client) :
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]