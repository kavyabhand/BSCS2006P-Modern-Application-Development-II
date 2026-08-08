from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student_profile = db.relationship("StudentProfile", back_populates="user", uselist=False)
    company_profile = db.relationship("CompanyProfile", back_populates="user", uselist=False)

class StudentProfile(db.Model):
    __tablename__ = "student_profiles"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), nullable=False, unique=True)
    branch = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20))
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    resume_filename = db.Column(db.String(255))
    about = db.Column(db.Text)

    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship("Application", back_populates="student")


class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    website = db.Column(db.String(255))
    hr_name = db.Column(db.String(100))
    hr_email = db.Column(db.String(120))
    hr_phone = db.Column(db.String(20))
    hr_position = db.Column(db.String(100))
    description = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default="pending")

    user = db.relationship("User", back_populates="company_profile")
    drives = db.relationship("PlacementDrive", back_populates="company")


class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"
    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey("company_profiles.id"), nullable=False)

    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text)
    required_skills = db.Column(db.Text)
    minimum_cgpa = db.Column(db.Float)
    eligible_branch = db.Column(db.String(50))
    eligible_year = db.Column(db.Integer)
    salary_lpa = db.Column(db.Float)
    application_deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default="pending")

    company = db.relationship("CompanyProfile", back_populates="drives")
    applications = db.relationship("Application", back_populates="drive")


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)

    status = db.Column(db.String(20), default="applied")
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("StudentProfile", back_populates="applications")
    drive = db.relationship("PlacementDrive", back_populates="applications")
    placement = db.relationship("Placement", back_populates="application", uselist=False)

    __table_args__ = (db.UniqueConstraint("student_id", "drive_id", name="unique_student_drive"),)


class Placement(db.Model):
    __tablename__ = "placements"
    id = db.Column(db.Integer, primary_key=True)

    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False, unique=True)

    offered_package = db.Column(db.Float)
    joining_date = db.Column(db.Date)
    offer_letter_filename = db.Column(db.String(255))
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)

    application = db.relationship("Application", back_populates="placement")