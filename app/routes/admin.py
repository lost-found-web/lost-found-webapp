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

    # USERS
    total_users = User.query.count()

    # ITEMS
    total_items = Item.query.count()
    lost_items = Item.query.filter_by(item_type="lost").count()
    found_items = Item.query.filter_by(item_type="found").count()
    recovered_items = Item.query.filter_by(status="recovered").count()
    active_items = Item.query.filter_by(status="active").count()

    users = User.query.all()
    items = Item.query.order_by(Item.created_at.desc()).all()

    return render_template(
        "admin/dashboard.html",
        users=users,
        items=items,
        total_users=total_users,
        total_items=total_items,
        lost_items=lost_items,
        found_items=found_items,
        recovered_items=recovered_items,
        active_items=active_items
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

@admin_bp.route("/user/block/<int:user_id>")
@login_required
def block_user(user_id):
    if not admin_required():
        return redirect(url_for("items.home"))

    user = User.query.get_or_404(user_id)
    user.is_blocked = True
    db.session.commit()

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/user/unblock/<int:user_id>")
@login_required
def unblock_user(user_id):
    if not admin_required():
        return redirect(url_for("items.home"))

    user = User.query.get_or_404(user_id)
    user.is_blocked = False
    db.session.commit()

    return redirect(url_for("admin.dashboard"))
