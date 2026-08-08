from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from extensions import db
from models import CompanyProfile, StudentProfile, PlacementDrive, User, Application
from tasks.reports import generate_monthly_report
from tasks.reminders import send_deadline_reminders

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/test")
def test():
    return jsonify({"message": "Admin route working"})


@admin_bp.route("/pending-companies", methods=["GET"])
@jwt_required()
def view_companies():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    companies = CompanyProfile.query.filter_by(approval_status="pending").all()

    company_list = []
    for company in companies:
        company_list.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "website": company.website,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
        })

    return jsonify({"companies": company_list}), 200


@admin_bp.route("/companies", methods=["GET"])
@jwt_required()
def search_companies():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    q = request.args.get("q", "")
    query = CompanyProfile.query

    if q:
        query = query.filter(
            db.or_(
                CompanyProfile.company_name.like(f"%{q}%"),
                CompanyProfile.industry.like(f"%{q}%")
            )
        )

    companies = query.all()

    company_list = []
    for company in companies:
        company_list.append({
            "id": company.id,
            "user_id": company.user_id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "approval_status": company.approval_status,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
        })

    return jsonify({"companies": company_list}), 200


@admin_bp.route("/approve-company/<int:company_id>", methods=["PUT"])
@jwt_required()
def approve_company(company_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    company = CompanyProfile.query.get(company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    if company.approval_status == "approved":
        return jsonify({"message": "Company is already approved"}), 400

    company.approval_status = "approved"
    db.session.commit()

    return jsonify({"message": "Company approved successfully"}), 200


@admin_bp.route("/reject-company/<int:company_id>", methods=["PUT"])
@jwt_required()
def reject_company(company_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    company = CompanyProfile.query.get(company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    if company.approval_status == "rejected":
        return jsonify({"message": "Company is already rejected"}), 400

    company.approval_status = "rejected"
    db.session.commit()

    return jsonify({"message": "Company rejected successfully"}), 200


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    total_students = StudentProfile.query.count()
    total_companies = CompanyProfile.query.count()
    total_drives = PlacementDrive.query.count()
    total_selected = Application.query.filter_by(status="selected").count()

    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_drives": total_drives,
        "total_selected": total_selected
    }), 200


@admin_bp.route("/pending-drives", methods=["GET"])
@jwt_required()
def view_pending_drives():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    drives = PlacementDrive.query.filter_by(status="pending").all()

    drive_list = []
    for drive in drives:
        drive_list.append({
            "id": drive.id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "minimum_cgpa": drive.minimum_cgpa,
            "deadline": str(drive.application_deadline),
            "status": drive.status
        })

    return jsonify({"drives": drive_list}), 200


@admin_bp.route("/approve-drive/<int:drive_id>", methods=["PUT"])
@jwt_required()
def approve_drive(drive_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    if drive.status == "approved":
        return jsonify({"message": "Drive already approved"}), 400

    drive.status = "approved"
    db.session.commit()

    return jsonify({"message": "Drive approved successfully"}), 200


@admin_bp.route("/reject-drive/<int:drive_id>", methods=["PUT"])
@jwt_required()
def reject_drive(drive_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    if drive.status == "rejected":
        return jsonify({"message": "Drive already rejected"}), 400

    drive.status = "rejected"
    db.session.commit()

    return jsonify({"message": "Drive rejected successfully"}), 200


@admin_bp.route("/all-drives", methods=["GET"])
@jwt_required()
def view_all_drives():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    q = request.args.get("q", "")
    query = PlacementDrive.query

    if q:
        query = query.filter(PlacementDrive.job_title.like(f"%{q}%"))

    drives = query.all()

    drive_list = []
    for drive in drives:
        drive_list.append({
            "id": drive.id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "minimum_cgpa": drive.minimum_cgpa,
            "deadline": str(drive.application_deadline),
            "status": drive.status,
            "applicants": len(drive.applications)
        })

    return jsonify({"drives": drive_list}), 200


@admin_bp.route("/close-drive/<int:drive_id>", methods=["PUT"])
@jwt_required()
def close_drive(drive_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    if drive.status == "closed":
        return jsonify({"message": "Drive already closed"}), 400

    drive.status = "closed"
    db.session.commit()

    return jsonify({"message": "Drive closed successfully"}), 200


@admin_bp.route("/students", methods=["GET"])
@jwt_required()
def view_students():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    q = request.args.get("q", "")
    query = StudentProfile.query

    if q:
        query = query.filter(
            db.or_(
                StudentProfile.full_name.like(f"%{q}%"),
                StudentProfile.roll_number.like(f"%{q}%")
            )
        )

    students = query.all()

    data = []
    for s in students:
        data.append({
            "id": s.id,
            "user_id": s.user_id,
            "name": s.full_name,
            "roll_number": s.roll_number,
            "branch": s.branch,
            "cgpa": s.cgpa,
            "phone": s.phone
        })

    return jsonify({"students": data}), 200


@admin_bp.route("/applications", methods=["GET"])
@jwt_required()
def view_applications():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    applications = Application.query.all()

    data = []
    for application in applications:
        data.append({
            "id": application.id,
            "student_name": application.student.full_name,
            "roll_number": application.student.roll_number,
            "company_name": application.drive.company.company_name,
            "job_title": application.drive.job_title,
            "status": application.status,
            "applied_at": str(application.applied_at)
        })

    return jsonify({"applications": data}), 200


@admin_bp.route("/blacklist-student/<int:user_id>", methods=["PUT"])
@jwt_required()
def blacklist_student(user_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)

    if not user or user.role != "student":
        return jsonify({"message": "Student not found"}), 404

    user.is_blacklisted = True
    db.session.commit()

    return jsonify({"message": "Student blacklisted"}), 200


@admin_bp.route("/blacklist-company/<int:user_id>", methods=["PUT"])
@jwt_required()
def blacklist_company(user_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)

    if not user or user.role != "company":
        return jsonify({"message": "Company not found"}), 404

    user.is_blacklisted = True
    db.session.commit()

    return jsonify({"message": "Company blacklisted"}), 200


@admin_bp.route("/deactivate-student/<int:user_id>", methods=["PUT"])
@jwt_required()
def deactivate_student(user_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)

    if not user or user.role != "student":
        return jsonify({"message": "Student not found"}), 404

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "Student deactivated"}), 200


@admin_bp.route("/deactivate-company/<int:user_id>", methods=["PUT"])
@jwt_required()
def deactivate_company(user_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)

    if not user or user.role != "company":
        return jsonify({"message": "Company not found"}), 404

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "Company deactivated"}), 200


@admin_bp.route("/report", methods=["GET"])
@jwt_required()
def report():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    result = generate_monthly_report.delay()

    return jsonify({"message": "Report generation started", "task_id": result.id}), 200


@admin_bp.route("/reminders", methods=["GET"])
@jwt_required()
def reminders():
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"message": "Access denied"}), 403

    result = send_deadline_reminders.delay()

    return jsonify({"message": "Reminders triggered", "task_id": result.id}), 200
