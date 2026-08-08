from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError
from models import User, StudentProfile, CompanyProfile
from extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/test")
def test():
    return jsonify({"message": "Hello World"})


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password or not role:
        return jsonify({"message": "Missing fields"}), 400

    if role not in ["student", "company"]:
        return jsonify({"message": "Invalid role"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    student_data = None
    company_data = None

    if role == "student":
        full_name = data.get("full_name")
        roll_number = data.get("roll_number")
        branch = data.get("branch")
        year = data.get("year")
        cgpa = data.get("cgpa")

        if not full_name or not roll_number or not branch or year is None or cgpa is None:
            return jsonify({"message": "All student fields are required"}), 400

        try:
            year = int(year)
            cgpa = float(cgpa)
        except (ValueError, TypeError):
            return jsonify({"message": "Year and CGPA must be valid numbers"}), 400

        if StudentProfile.query.filter_by(roll_number=roll_number).first():
            return jsonify({"message": "Roll number already exists"}), 400

        student_data = {
            "full_name": full_name,
            "roll_number": roll_number,
            "branch": branch,
            "year": year,
            "cgpa": cgpa
        }

    elif role == "company":
        company_name = data.get("company_name")

        if not company_name:
            return jsonify({"message": "Company name is required"}), 400

        company_data = {
            "company_name": company_name,
            "industry": data.get("industry"),
            "location": data.get("location"),
            "website": data.get("website"),
            "hr_name": data.get("hr_name"),
            "hr_email": data.get("hr_email")
        }

    hashed_password = generate_password_hash(password)

    new_user = User(
        email=email,
        password_hash=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.flush()

    if student_data:
        student = StudentProfile(user_id=new_user.id, **student_data)
        db.session.add(student)

    elif company_data:
        company = CompanyProfile(user_id=new_user.id, **company_data)
        db.session.add(company)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email or roll number already exists"}), 400

    return jsonify({"message": f"{role.capitalize()} registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    if user.is_blacklisted:
        return jsonify({"message": "Account is blacklisted"}), 403

    if not user.is_active:
        return jsonify({"message": "Account is deactivated"}), 403

    if not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "is_blacklisted": user.is_blacklisted}
    )

    return jsonify({"message": "Login successful", "access_token": access_token, "role": user.role}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    claims = get_jwt()

    return jsonify({
        "user_id": user_id,
        "role": claims["role"],
        "is_blacklisted": claims.get("is_blacklisted", False)
    })


@auth_bp.route("/student-dashboard", methods=["GET"])
@jwt_required()
def student_dashboard():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({"message": "Welcome Student!"})