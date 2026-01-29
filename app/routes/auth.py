from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        full_name = request.form["full_name"]
        contact = request.form["contact"]
        password = request.form["password"]

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists", "danger")
            return redirect(url_for("auth.register"))

        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            contact_number=contact,
            password=generate_password_hash(password),
            role="user",
            is_blocked=False
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")



@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
           flash("Invalid credentials", "danger")
           return redirect(url_for("auth.login"))

        if user.is_blocked:
           flash("Your account has been blocked by admin.", "danger")
           return redirect(url_for("auth.login"))


        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("items.home"))

        flash("Invalid email or password", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("items.home"))

from flask_login import login_required, current_user
from app.extensions import db


