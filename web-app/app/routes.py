"""
Web application routes module.
This module defines all the routes and their handling logic.
"""

import io
import base64

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_file,
    make_response,
)
from app import app
from app.models import Database
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def index():
    """Render the main page of the application."""
    db = Database()

    history = None

    if "user" in session:
        history = db.get_latest_results(session["user"])

    return render_template("index.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = Database()
        user = db.find_user({"email": email})

        if user and check_password_hash(user["password"], password):
            session["user"] = email
            return redirect(url_for("index"))
        flash("Invalid email or password")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = Database()
        if db.find_user({"email": email}):
            flash("Email already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        db.add_user({"email": email, "password": hashed_password})
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    """Handle user logout"""
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Handle picture upload requests.
    Requires user authentication.
    """
    if "user" not in session:
        return redirect(url_for("login"))

    db = Database()
    result = None
    user_id = session["user"]

    if request.method == "POST" and "image" in request.files:
        image_file = request.files["image"]

        if image_file:
            # Save the image and get detection result
            image_data = image_file.read()
            result = db.save_picture(user_id, image_data)

    return render_template("upload.html", result=result)


@app.route("/camera", methods=["GET", "POST"])
def camera():
    """
    Handle camera requests.
    Requires user authentication.
    """
    if "user" not in session:
        return redirect(url_for("login"))

    db = Database()
    user_id = session["user"]

    if request.method == "POST":
        data = request.get_json()

        if "image" in data:
            try:
                image_data = base64.b64decode(data["image"].split(",")[1])
                db.save_picture(user_id, image_data)
                return make_response("OK", 200)
            except Exception as e:
                return make_response(f"Error saving picture: {e}", 500)

    else:
        latest = db.get_latest_results(session["user"], limit=1)
        return render_template("camera.html", latest=latest)


@app.route("/images/<image_id>")
def get_image(image_id):
    """Get image from database"""
    try:
        db = Database()
        image_data = db.get_image(image_id)
        if image_data:
            return send_file(io.BytesIO(image_data), mimetype="image/jpeg")
    except Exception as e:
        print(f"Error getting image: {e}")
    return "Image not found", 404
