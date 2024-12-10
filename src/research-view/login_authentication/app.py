from flask import Flask, request, redirect, url_for, session, render_template
import requests
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure random key
app.permanent_session_lifetime = timedelta(minutes=30)

# FastAPI base URL
FASTAPI_URL = "http://localhost:8000"

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Call the FastAPI login endpoint
        response = requests.post(f"{FASTAPI_URL}/login", data={"username": email, "password": password})
        if response.status_code == 200:
            session["token"] = response.json()["access_token"]
            session.permanent = True
            return redirect(url_for("dashboard"))
        else:
            return f"Login failed: {response.text}", 401

    return render_template("login.html", title="Admin Portal")

@app.route("/dashboard")
def dashboard():
    token = session.get("token")
    if not token:
        return redirect(url_for("login"))
    return render_template("dashboard.html", title="Admin Portal")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)