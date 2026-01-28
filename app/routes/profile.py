from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.full_name = request.form.get("full_name")
        current_user.contact_number = request.form.get("contact_number")
        current_user.email = request.form.get("email")

        db.session.commit()
        flash("Profile updated successfully", "success")

        return redirect(url_for("profile.profile"))

    return render_template("profile.html")
