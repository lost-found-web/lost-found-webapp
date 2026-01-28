from datetime import datetime
from app.extensions import db

class Item(db.Model):

    

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    item_type = db.Column(db.String(20), nullable=False)  # lost / found
    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    date_reported = db.Column(db.Date, nullable=False)

    contact = db.Column(db.String(20), nullable=False)

    image = db.Column(db.String(255))  # filename
    status = db.Column(db.String(20), default="active",nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="items",lazy=True)
