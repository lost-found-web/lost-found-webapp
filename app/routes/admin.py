from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.models.user import User
from app.models.item import Item
from app.extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Admin access guard
def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


@admin_bp.route("/")
@login_required
def dashboard():
    if not admin_required():
        return redirect(url_for("items.home"))

    users = User.query.all()
    items = Item.query.all()

    return render_template(
        "admin/dashboard.html",
        users=users,
        items=items
    )


@admin_bp.route("/item/delete/<int:item_id>")
@login_required
def delete_item(item_id):
    if not admin_required():
        return redirect(url_for("items.home"))

    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("admin.dashboard"))
