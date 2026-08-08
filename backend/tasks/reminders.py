import json
import urllib.request
from datetime import date, timedelta
from celery_app import celery
from models import PlacementDrive, StudentProfile, User
from mail import send_email
from flask import current_app

@celery.task
def send_deadline_reminders():
    today = date.today()
    soon = today + timedelta(days=3)

    drives = PlacementDrive.query.filter(
        PlacementDrive.status == "approved",
        PlacementDrive.application_deadline >= today,
        PlacementDrive.application_deadline <= soon
    ).all()

    students = StudentProfile.query.all()
    count = 0

    for drive in drives:
        msg = f"Reminder: {drive.job_title} at {drive.company.company_name} deadline is {drive.application_deadline}"

        webhook = current_app.config.get("GOOGLE_CHAT_WEBHOOK", "")
        if webhook:
            try:
                data = json.dumps({"text": msg}).encode()
                req = urllib.request.Request(webhook, data=data, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req, timeout=10)
            except Exception as e:
                print(f"Webhook failed (app continues): {e}")

        for student in students:
            user = User.query.get(student.user_id)
            if user and user.email:
                send_email(user.email, "Placement Drive Deadline Reminder", msg)
                count += 1

    return f"Sent reminders for {len(drives)} drives to {count} students"
