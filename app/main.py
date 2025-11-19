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
