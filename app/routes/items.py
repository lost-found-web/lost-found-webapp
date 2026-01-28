from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os

from app.extensions import db
from app.models.item import Item

from flask import current_app
from flask import request


items_bp = Blueprint('items', __name__)


@items_bp.route("/")
def home():
    search = request.args.get("search", "")
    category = request.args.get("category", "")
    location = request.args.get("location", "")

    query = Item.query.filter_by(status="active")

    if search:
        query = query.filter(Item.item_name.ilike(f"%{search}%"))

    if category:
        query = query.filter_by(category=category)

    if location:
        query = query.filter(Item.location.ilike(f"%{location}%"))

    items = query.order_by(Item.created_at.desc()).all()

    return render_template(
        "home.html",
        items=items,
        search=search,
        category=category,
        location=location
    )


@items_bp.route("/report/<item_type>", methods=["GET", "POST"])
@login_required
def report_item(item_type):
    if item_type not in ["lost", "found"]:
        return redirect(url_for("items.home"))

    if request.method == "POST":
        # ---------- IMAGE HANDLING ----------
        image_file = request.files.get("image")
        filename = None

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
            image_file.save(image_path)

        # ---------- SAVE ITEM ----------
        new_item = Item(
            user_id=current_user.id,
            item_type=item_type,
            item_name=request.form["item_name"],
            category=request.form["category"],
            description=request.form["description"],
            location=request.form["location"],
            contact=request.form["contact"],
            date_reported=datetime.strptime(
                request.form["date_reported"], "%Y-%m-%d"
            ).date(),
            image=filename,
            status="active"
        )

        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for("items.home"))

    return render_template("report_item.html", item_type=item_type)
@items_bp.route("/item/<int:item_id>")
def item_details(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template("item_details.html", item=item)
@items_bp.route("/item/<int:item_id>/recover", methods=["POST"])
@login_required
def mark_recovered(item_id):
    item = Item.query.get_or_404(item_id)

    # Only owner can mark as recovered
    if item.user_id != current_user.id:
        return redirect(url_for("items.home"))

    item.status = "recovered"
    db.session.commit()

    return redirect(url_for("items.item_details", item_id=item.id))

@items_bp.route("/item/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    # Only owner can delete
    if item.user_id != current_user.id:
        return redirect(url_for("items.home"))

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("items.home"))

@items_bp.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)

    # Only owner can edit
    if item.user_id != current_user.id:
        return redirect(url_for("items.home"))

    if request.method == "POST":
        item.item_name = request.form["item_name"]
        item.category = request.form["category"]
        item.description = request.form["description"]
        item.location = request.form["location"]
        item.contact = request.form["contact"]
        item.date_reported = datetime.strptime(
            request.form["date_reported"], "%Y-%m-%d"
        ).date()

        # Optional image update
        image_file = request.files.get("image")
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
            image_file.save(image_path)
            item.image = filename

        db.session.commit()
        return redirect(url_for("items.item_details", item_id=item.id))

    return render_template("edit_item.html", item=item)
