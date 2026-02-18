from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os
from dotenv import load_dotenv
import random

load_dotenv()
from functools import wraps
from flask import jsonify


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # keep this securee

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

# ----------------------
# Login Required Decorator
# ----------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ----------------------
# Login Page
# ----------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if "idToken" in data:
            session["user"] = data["email"]
            session["token"] = data["idToken"]
            return redirect(url_for("dashboard"))
        else:
            error = data.get("error", {}).get("message", "Login failed")

    return render_template("login.html", error=error)

# -----------------------
# Dashboard (Protected)
# -----------------------
@app.route("/dashboard")
@login_required
def dashboard():
    token = session.get("token")

    # If DB requires auth
    params = {"auth": token}

    response = requests.get(FIREBASE_DB_URL, params=params)
    data = response.json()

    return render_template("dashboard.html", user=session["user"], data=data)


@app.route("/api/data")
@login_required
def get_realtime_data():
    token = session.get("token")

    response = requests.get(
        FIREBASE_DB_URL,
        params={"auth": token}
    )

    data = response.json()
    return data

@app.route("/add-event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":

        event_name = request.form.get("event_name")
        event_date = request.form.get("event_date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        handler = request.form.get("handler")
        lic_key = request.form.get("lic_key")

        if not all([event_name, event_date, start_time, end_time, handler, lic_key]):
            return render_template("add_event.html", error="All fields are required")

        event_data = {
            "event_name": event_name,
            "event_date": event_date,  # DD/MM/YYYY
            "event_start_time_": start_time,
            "event_end_time_to": end_time,
            "handling_person_name": handler,
            "lic_key": int(lic_key),
            "data": {}
        }

        firebase_url = f"https://humananalysisv0-default-rtdb.firebaseio.com/Events/{lic_key}.json"

        requests.put(
            firebase_url,
            json=event_data,
            params={"auth": session.get("token")}
        )

        return redirect(url_for("dashboard"))

    return render_template("add_event.html")


@app.route("/generate-license-key")
@login_required
def generate_license_key():
    token = session.get("token")

    while True:
        # Generate 6-digit unique key
        lic_key = random.randint(10000, 999999999)

        # Check if key exists in Firebase
        check_url = f"https://humananalysisv0-default-rtdb.firebaseio.com/Events/{lic_key}.json"
        response = requests.get(check_url, params={"auth": token})

        if response.json() is None:
            return jsonify({"lic_key": lic_key})


# ----------------------
# Logout
# ----------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)
