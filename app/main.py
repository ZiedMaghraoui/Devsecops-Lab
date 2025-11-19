from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello Secure DevSecOps!"

# XSS vulnerability
@app.route("/vulnerable")
def vulnerable():
    user_input = request.args.get("input", "")
    return f"You sent: {user_input}"

# Command injection
@app.route("/ping")
def ping():
    host = request.args.get("host")
    os.system(f"ping -c 1 {host}")
    return "Ping sent!"

@app.route("/sum")
def sum():
    a = request.args.get("a", 0)
    b = request.args.get("b", 0)
    return str(int(a) + int(b))

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
