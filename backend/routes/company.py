from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from extensions import db
from models import CompanyProfile, PlacementDrive, Application, Placement

company_bp = Blueprint("company", __name__)

def get_company(user_id):
    return CompanyProfile.query.filter_by(user_id=user_id).first()

def require_approved_company(user_id):
    company = get_company(user_id)
    if not company:
        return None, {"message": "Create your company profile first"}, 400
    if company.approval_status != "approved":
        return None, {"message": "Company not approved yet"}, 403
    return company, None, None

@company_bp.route("/test")
def test():
    return jsonify({"message": "Company route working"})


@company_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_profile():
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    data = request.get_json()
    company_name = data.get("company_name")
    industry = data.get("industry")
    location = data.get("location")
    website = data.get("website")
    hr_name = data.get("hr_name")
    hr_email = data.get("hr_email")
    hr_phone = data.get("hr_phone")
    hr_position = data.get("hr_position")
    description = data.get("description")

    existing_profile = CompanyProfile.query.filter_by(user_id=user_id).first()
    if existing_profile:
        return jsonify({"message": "Profile already exists"}), 400

    profile = CompanyProfile(user_id=user_id, company_name=company_name, industry=industry, location=location, website=website, hr_name=hr_name, hr_email=hr_email, hr_phone=hr_phone, hr_position=hr_position, description=description)
    db.session.add(profile)
    db.session.commit()
    return jsonify({"message": "Company profile created successfully"}), 201


@company_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Profile not found"}), 404

    return jsonify({
        "company_name": company.company_name,
        "industry": company.industry or "",
        "location": company.location or "",
        "website": company.website or "",
        "hr_name": company.hr_name or "",
        "hr_email": company.hr_email or "",
        "hr_phone": company.hr_phone or "",
        "hr_position": company.hr_position or "",
        "description": company.description or "",
        "approval_status": company.approval_status
    }), 200


@company_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Create your company profile first"}), 400

    data = request.get_json()

    if data.get("industry"):
        company.industry = data.get("industry")
    if data.get("location"):
        company.location = data.get("location")
    if data.get("website"):
        company.website = data.get("website")
    if data.get("hr_name"):
        company.hr_name = data.get("hr_name")
    if data.get("hr_email"):
        company.hr_email = data.get("hr_email")
    if data.get("hr_phone"):
        company.hr_phone = data.get("hr_phone")
    if data.get("hr_position"):
        company.hr_position = data.get("hr_position")
    if data.get("description"):
        company.description = data.get("description")

    db.session.commit()

    return jsonify({"message": "Company profile updated successfully"}), 200


@company_bp.route("/drives", methods=["POST"])
@jwt_required()
def create_drive():
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403
        
    user_id = int(get_jwt_identity())

    company = CompanyProfile.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"message": "Create your company profile first"}), 400

    if company.approval_status != "approved":
        return jsonify({"message": "Company not approved yet"}), 403

    data = request.get_json()
    job_title = data.get("job_title")
    job_description = data.get("job_description")
    required_skills = data.get("required_skills")
    minimum_cgpa = data.get("minimum_cgpa")
    eligible_branch = data.get("eligible_branch")
    eligible_year = data.get("eligible_year")
    salary_lpa = data.get("salary_lpa")
    application_deadline = data.get("application_deadline")

    if not job_title:
        return jsonify({"message": "Job title is required"}), 400

    if not application_deadline:
        return jsonify({"message": "Application deadline is required"}), 400

    try:
        application_deadline = datetime.strptime(application_deadline, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid deadline date"}), 400

    try:
        if minimum_cgpa not in (None, ""):
            minimum_cgpa = float(minimum_cgpa)
        else:
            minimum_cgpa = None

        if eligible_year not in (None, ""):
            eligible_year = int(eligible_year)
        else:
            eligible_year = None

        if salary_lpa not in (None, ""):
            salary_lpa = float(salary_lpa)
        else:
            salary_lpa = None
    except ValueError:
        return jsonify({"message": "Invalid number in CGPA, year, or salary"}), 400

    if not eligible_branch:
        eligible_branch = None

    drive = PlacementDrive(company_id=company.id, job_title=job_title, job_description=job_description, required_skills=required_skills, minimum_cgpa=minimum_cgpa, eligible_branch=eligible_branch, eligible_year=eligible_year, salary_lpa=salary_lpa, application_deadline=application_deadline)
    db.session.add(drive)
    db.session.commit()
    return jsonify({"message": "Placement drive created successfully"}), 201
    

@company_bp.route("/applications", methods=["GET"])
@jwt_required()
def view_applications():
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403
        
    user_id = int(get_jwt_identity())

    company, msg, code = require_approved_company(user_id)
    if msg:
        return jsonify(msg), code

    drives = company.drives
    application_list = []
    for drive in drives:
        for application in drive.applications:
            student = application.student
            application_list.append({
                "application_id": application.id,
                "student_name": student.full_name,
                "roll_number": student.roll_number,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "job_title": drive.job_title,
                "status": application.status
            })
    return jsonify({"applications": application_list}), 200


@company_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())

    company = get_company(user_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    total_drives = PlacementDrive.query.filter_by(company_id=company.id).count()

    total_applications = (
        Application.query.join(PlacementDrive)
        .filter(PlacementDrive.company_id == company.id)
        .count()
    )

    drive_stats = []
    for drive in company.drives:
        drive_stats.append({
            "id": drive.id,
            "job_title": drive.job_title,
            "status": drive.status,
            "applicants": len(drive.applications)
        })

    return jsonify({
        "company_name": company.company_name,
        "approval_status": company.approval_status,
        "total_drives": total_drives,
        "total_applications": total_applications,
        "drives": drive_stats
    }), 200


@company_bp.route("/drives", methods=["GET"])
@jwt_required()
def view_drives():
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())

    company, msg, code = require_approved_company(user_id)
    if msg:
        return jsonify(msg), code

    drives = []

    for drive in company.drives:
        drives.append({
            "id": drive.id,
            "job_title": drive.job_title,
            "status": drive.status,
            "deadline": str(drive.application_deadline),
            "applicants": len(drive.applications)
        })

    return jsonify({"drives": drives})


@company_bp.route("/application/<int:application_id>/status", methods=["PUT"])
@jwt_required()
def update_application_status(application_id):
    claims = get_jwt()

    if claims["role"] != "company":
        return jsonify({"message": "Access denied"}), 403

    user_id = int(get_jwt_identity())

    company, msg, code = require_approved_company(user_id)
    if msg:
        return jsonify(msg), code

    data = request.get_json()
    new_status = data.get("status")

    valid_status = ["applied", "shortlisted", "rejected", "interview", "selected"]

    if new_status not in valid_status:
        return jsonify({"message": "Invalid status"}), 400

    application = Application.query.get(application_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    if application.drive.company_id != company.id:
        return jsonify({"message": "Access denied"}), 403

    application.status = new_status

    if new_status == "selected" and not application.placement:
        placement = Placement(application_id=application.id, offered_package=application.drive.salary_lpa)
        db.session.add(placement)

    db.session.commit()

    return jsonify({"message": "Status updated successfully"}), 200
