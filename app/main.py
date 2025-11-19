from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <a href="/vulnerable?input=<script>alert('xss')</script>">Vulnerable</a>
    <a href="/sum?a=1&b=2">Sum</a>
    <a href="/redirect?url=http://google.com">Redirect</a>
    <a href="/login">Login</a>
    """


@app.route("/vulnerable")
def vulnerable():
    user_input = request.args.get("input", "")
    safe_input = escape(user_input)
    return f"You sent: {safe_input}"


@app.route("/redirect")
def redirect_me():
    url = request.args.get("url")
    return redirect(url)


@app.route("/login")
def login():
    """
    Handle login request.

    Returns a response with a "Logged in" message and sets a session cookie
    with the value "abc123". Note that the cookie is missing the Secure and HttpOnly
    flags, making it vulnerable to interception and tampering.
    """
    resp = make_response("Logged in")
    resp.set_cookie("session", "abc123")   # Missing Secure, HttpOnly
    return resp


# simple auth bypass or insecure endpoint for SAST/DAST
@app.route("/admin")
def admin():
    token = request.args.get("token", "")
    if token == "1234":  # Hardcoded secret
        return "Welcome admin!"
    return "Access denied."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
