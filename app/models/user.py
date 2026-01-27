from flask_login import UserMixin
from datetime import datetime
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20))
    role = db.Column(db.String(20), default="user")  # user / admin

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
