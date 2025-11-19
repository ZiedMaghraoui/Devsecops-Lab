from app.main import app

def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data

def test_sum_route():
    client = app.test_client()
    response = client.get("/sum?a=1&b=2")
    assert response.status_code == 200
    assert b"3" in response.data