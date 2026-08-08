from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
from datetime import date
from extensions import db, cache
from models import StudentProfile, PlacementDrive, Application, CompanyProfile, Placement
from celery.result import AsyncResult
from celery_app import celery
from tasks.export import export_applications
import json
import os

student_bp = Blueprint("student", __name__)

@student_bp.route("/test")
def test():
    return jsonify({"message": "Student route working"})


@student_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_profile():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    data = request.get_json()
    full_name = data.get("full_name")
    roll_number = data.get("roll_number")
    branch = data.get("branch")
    year = data.get("year")
    cgpa = data.get("cgpa")
    phone = data.get("phone")
    skills = data.get("skills")
    experience = data.get("experience")
    about = data.get("about")

    existing_profile = StudentProfile.query.filter_by(user_id=user_id).first()

    if existing_profile:
        return jsonify({"message": "Profile already exists"}), 400

    profile = StudentProfile(user_id=user_id, full_name=full_name, roll_number=roll_number, branch=branch, year=year, cgpa=cgpa, phone=phone, skills=skills, experience=experience, about=about)
    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "Student profile created successfully"}), 201


@student_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Profile not found"}), 404

    return jsonify({
        "full_name": student.full_name,
        "roll_number": student.roll_number,
        "branch": student.branch,
        "year": student.year,
        "cgpa": student.cgpa,
        "phone": student.phone or "",
        "skills": student.skills or "",
        "experience": student.experience or "",
        "about": student.about or "",
        "resume_filename": student.resume_filename or ""
    }), 200


@student_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    data = request.get_json()

    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Profile not found"}), 404

    if data.get("full_name"):
        student.full_name = data.get("full_name")
    if data.get("roll_number"):
        student.roll_number = data.get("roll_number")
    if data.get("branch"):
        student.branch = data.get("branch")
    if data.get("year"):
        student.year = data.get("year")
    if data.get("cgpa"):
        student.cgpa = data.get("cgpa")
    if data.get("phone"):
        student.phone = data.get("phone")
    if data.get("skills"):
        student.skills = data.get("skills")
    if data.get("experience"):
        student.experience = data.get("experience")
    if data.get("about"):
        student.about = data.get("about")

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200


@student_bp.route("/resume", methods=["POST"])
@jwt_required()
def upload_resume():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Create profile first"}), 404

    if "resume" not in request.files:
        return jsonify({"message": "No file provided"}), 400

    file = request.files["resume"]
    filename = secure_filename(file.filename)

    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads", "resumes")
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))

    student.resume_filename = filename
    db.session.commit()

    return jsonify({"message": "Resume uploaded successfully", "filename": filename}), 200


@student_bp.route("/companies", methods=["GET"])
@jwt_required()
def search_companies():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    q = request.args.get("q", "")
    query = CompanyProfile.query.filter_by(approval_status="approved")

    if q:
        query = query.filter(CompanyProfile.company_name.like(f"%{q}%"))

    companies = query.all()

    company_list = []
    for company in companies:
        company_list.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "website": company.website
        })

    return jsonify({"companies": company_list}), 200


@student_bp.route("/drives", methods=["GET"])
@jwt_required()
def view_drives():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    q = request.args.get("q", "")
    branch = request.args.get("branch", "")

    use_cache = not q and not branch
    cache_key = f"student_drives_{user_id}"

    if use_cache:
        cached = cache.get(cache_key)
        if cached:
            return jsonify({"drives": json.loads(cached)}), 200

    student = StudentProfile.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"message": "Create profile first"}), 404

    query = PlacementDrive.query.filter_by(status="approved")

    if q:
        query = query.filter(PlacementDrive.job_title.like(f"%{q}%"))

    drives = query.all()
    drive_list = []

    for drive in drives:
        if branch and drive.eligible_branch and drive.eligible_branch != branch:
            continue

        if drive.eligible_branch and student.branch != drive.eligible_branch:
            eligible = False
        elif drive.eligible_year and student.year != drive.eligible_year:
            eligible = False
        elif drive.minimum_cgpa and student.cgpa < drive.minimum_cgpa:
            eligible = False
        elif drive.application_deadline and drive.application_deadline < date.today():
            eligible = False
        else:
            eligible = True

        already_applied = Application.query.filter_by(student_id=student.id, drive_id=drive.id).first() is not None

        drive_list.append({
            "id": drive.id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "minimum_cgpa": drive.minimum_cgpa,
            "eligible_branch": drive.eligible_branch,
            "eligible_year": drive.eligible_year,
            "salary_lpa": drive.salary_lpa,
            "deadline": str(drive.application_deadline),
            "status": drive.status,
            "eligible": eligible,
            "already_applied": already_applied
        })

    if use_cache:
        cache.set(cache_key, json.dumps(drive_list), timeout=60)

    return jsonify({"drives": drive_list}), 200


@student_bp.route("/apply/<int:drive_id>", methods=["POST"])
@jwt_required()
def apply_drive(drive_id):
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"message": "Create your student profile first"}), 404

    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Placement drive not found"}), 404

    if drive.status != "approved":
        return jsonify({"message": "This placement drive is not available"}), 403

    if drive.application_deadline and drive.application_deadline < date.today():
        return jsonify({"message": "Application deadline has passed"}), 403

    if drive.eligible_branch and student.branch != drive.eligible_branch:
        return jsonify({"message": "You are not eligible for this drive"}), 403

    if drive.eligible_year and student.year != drive.eligible_year:
        return jsonify({"message": "You are not eligible for this drive"}), 403

    if drive.minimum_cgpa and student.cgpa < drive.minimum_cgpa:
        return jsonify({"message": "You are not eligible for this drive"}), 403

    existing_application = Application.query.filter_by(student_id=student.id, drive_id=drive.id).first()
    if existing_application:
        return jsonify({"message": "You have already applied for this drive"}), 400

    application = Application(student_id=student.id, drive_id=drive.id)
    db.session.add(application)
    db.session.commit()
    cache.delete(f"student_drives_{user_id}")
    return jsonify({"message": "Application submitted successfully"}), 201


@student_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())

    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student profile not found"}), 404

    total_applications = Application.query.filter_by(student_id=student.id).count()

    return jsonify({
        "student_name": student.full_name,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "total_applications": total_applications
    }), 200


@student_bp.route("/applications", methods=["GET"])
@jwt_required()
def application_history():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())

    student = StudentProfile.query.filter_by(user_id=user_id).first()

    applications = []

    for application in student.applications:
        applications.append({
            "company": application.drive.company.company_name,
            "job_title": application.drive.job_title,
            "status": application.status,
            "applied_at": str(application.applied_at)
        })

    return jsonify({"applications": applications}), 200


@student_bp.route("/placements", methods=["GET"])
@jwt_required()
def placement_history():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Profile not found"}), 404

    placements = []

    for application in student.applications:
        if application.status == "selected" and application.placement:
            placements.append({
                "company": application.drive.company.company_name,
                "job_title": application.drive.job_title,
                "offered_package": application.placement.offered_package,
                "placed_at": str(application.placement.placed_at)
            })

    return jsonify({"placements": placements}), 200


@student_bp.route("/export", methods=["POST"])
@jwt_required()
def export():
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Create profile first"}), 404

    result = export_applications.delay(student.id)

    return jsonify({"message": "Export started", "task_id": result.id}), 200


@student_bp.route("/export/<task_id>", methods=["GET"])
@jwt_required()
def export_status(task_id):
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    result = AsyncResult(task_id, app=celery)

    if result.state in ["PENDING", "STARTED"]:
        return jsonify({"status": "processing"}), 200

    if result.state == "SUCCESS":
        return jsonify({"status": "done", "filename": result.result}), 200

    return jsonify({"status": "failed"}), 500


@student_bp.route("/export/download/<filename>", methods=["GET"])
@jwt_required()
def download_export(filename):
    claims = get_jwt()

    if claims["role"] != "student":
        return jsonify({"message": "Access denied"}), 403

    exports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
    return send_from_directory(exports_dir, filename, as_attachment=True)
