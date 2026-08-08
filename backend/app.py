import os
from flask import Flask, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from config import Config
from extensions import db, jwt, cors, cache
from routes.auth import auth_bp
from routes.student import student_bp
from routes.company import company_bp
from routes.admin import admin_bp
from werkzeug.security import generate_password_hash
from models import User
from celery_app import init_celery, celery

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    cache.init_app(app)
    init_celery(app)

    os.makedirs(os.path.join(os.path.dirname(__file__), "uploads", "resumes"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "exports"), exist_ok=True)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(company_bp, url_prefix="/company")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.before_request
    def enforce_active_user():
        if not request.headers.get("Authorization", "").startswith("Bearer "):
            return None
        try:
            verify_jwt_in_request()
            user = User.query.get(int(get_jwt_identity()))
            if user and (user.is_blacklisted or not user.is_active):
                return jsonify({"message": "Account blocked"}), 403
        except Exception:
            return None
    
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(role="admin").first()

        if not admin:
            admin = User(
                email="admin@placement.com",
                password_hash=generate_password_hash("admin123"),
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()

            print("Admin created successfully.")

    @app.route("/")
    def home():
        return "Running woho"

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)