from flask import Flask

from config import Config

from database.db import (
    db,
    bcrypt,
    login_manager
)

from database.model import User

from routes.prediction import prediction
from routes.auth import auth
from routes.doctor import doctor
from routes.admin import admin
from routes.reports import reports


app = Flask(__name__)

app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(prediction)
app.register_blueprint(doctor)
app.register_blueprint(admin)
app.register_blueprint(reports)
from flask import redirect, url_for

@app.route("/")
def index():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":

   # Create database and default admin (runs both locally and on Render)
with app.app_context():
    db.create_all()

    if not User.query.filter_by(email="pareekanubhav22@gmail.com").first():
        default_admin = User(
            full_name="Admin",
            email="pareekanubhav22@gmail.com",
            password=bcrypt.generate_password_hash("Admin@2006").decode("utf-8"),
            role="admin"
        )

        db.session.add(default_admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)