from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return f"Hello from Backend Pod! Hostname: {socket.gethostname()}"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/login")
def login():
    return "Login Service"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5112)
