import csv
import os
from datetime import datetime
from celery_app import celery
from models import Application, StudentProfile, User
from mail import send_email

@celery.task
def export_applications(student_id):
    apps = Application.query.filter_by(student_id=student_id).all()
    student = StudentProfile.query.get(student_id)

    exports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
    os.makedirs(exports_dir, exist_ok=True)

    filename = f"student_{student_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = os.path.join(exports_dir, filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Student ID", "Company Name", "Drive Title", "Application Status", "Applied Date"])
        for a in apps:
            writer.writerow([
                student_id,
                a.drive.company.company_name,
                a.drive.job_title,
                a.status,
                str(a.applied_at)
            ])

    user = User.query.get(student.user_id)
    if user:
        send_email(user.email, "Export Complete", f"Your application export is ready: {filename}")

    return filename
