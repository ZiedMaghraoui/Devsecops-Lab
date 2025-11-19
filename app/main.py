from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello Secure DevSecOps!"

# Reflects user input directly → XSS vulnerability
@app.route("/vulnerable")
def vulnerable():
    user_input = request.args.get("input", "")
    safe_input = escape(user_input)
    return f"You sent: {safe_input}"

@app.route("/sum")
def sum():
    a = request.args.get("a", 0)
    b = request.args.get("b", 0)
    return str(int(a) + int(b))

@app.route("/redirect")
def redirect_me():
    url = request.args.get("url")
    return redirect(url)


@app.route("/login")
def login():
    resp = make_response("Logged in")
    resp.set_cookie("session", "abc123")   # Missing Secure, HttpOnly
    return resp



# Optional: simple auth bypass or insecure endpoint for SAST/DAST
@app.route("/admin")
def admin():
    token = request.args.get("token", "")
    if token == "1234":  # Hardcoded secret
        return "Welcome admin!"
    return "Access denied."

if __name__ == "__main__":
    # Bind to all interfaces for Docker + ZAP
    app.run(host="0.0.0.0", port=8000)
