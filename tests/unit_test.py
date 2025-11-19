from app.main import app

def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    # Check required links
    expected_links = [
        '/vulnerable',
        '/sum',
        '/redirect?url=',
        '/login'
    ]
    for link in expected_links:
        assert link in html, f"Missing link: {link}"

def test_vulnerable_route_escapes_input():
    client = app.test_client()
    payload = "<script>alert('xss')</script>"
    response = client.get(f"/vulnerable?input={payload}")
    assert response.status_code == 200
    # The payload should NOT appear unescaped
    assert payload not in response.text
    # The payload should appear escaped
    assert "&lt;script&gt;" in response.text
    assert "&lt;/script&gt;" in response.text

def test_sum_route():
    client = app.test_client()
    response = client.get("/sum?a=1&b=2")
    assert response.status_code == 200
    assert b"3" in response.data