from database.db import db
from flask_login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
    )

    age = db.Column(db.Integer)

    gender = db.Column(db.String(20))

    phone = db.Column(db.String(20))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<User {self.email}>"


class PredictionHistory(db.Model):

    __tablename__ = "prediction_history"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    symptoms = db.Column(db.Text, nullable=False)

    predicted_disease = db.Column(
        db.String(150),
        nullable=False
    )

    confidence = db.Column(db.Float)

    prediction_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship(
    "User",
    backref=db.backref(
        "predictions",
        lazy=True,
        cascade="all, delete-orphan"
    )
)

    def __repr__(self):
        return f"<Prediction {self.predicted_disease}>"