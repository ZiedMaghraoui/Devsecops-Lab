from app.main import app

def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data

def test_vulnerable():
    client = app.test_client()
    response = client.get("/vulnerable?input=<script>alert('XSS')</script>")
    assert b"You sent: &lt;script&gt;alert('XSS')&lt;/script&gt;" in response.data
