from datetime import datetime
from celery_app import celery
from models import Application, User
from mail import send_email
from flask import current_app
from extensions import db

@celery.task
def generate_monthly_report():
    now = datetime.utcnow()
    start = datetime(now.year, now.month, 1)

    if now.month == 12:
        end = datetime(now.year + 1, 1, 1)
    else:
        end = datetime(now.year, now.month + 1, 1)

    drives_conducted = (
        db.session.query(Application.drive_id)
        .filter(Application.applied_at >= start, Application.applied_at < end)
        .distinct()
        .count()
    )

    total_applied = Application.query.filter(
        Application.applied_at >= start,
        Application.applied_at < end
    ).count()

    total_selected = Application.query.filter(
        Application.status == "selected",
        Application.applied_at >= start,
        Application.applied_at < end
    ).count()

    html = f"""
    <html><body>
    <h2>Monthly Placement Report - {now.strftime('%B %Y')}</h2>
    <p>Drives conducted: {drives_conducted}</p>
    <p>Students applied: {total_applied}</p>
    <p>Students selected: {total_selected}</p>
    </body></html>
    """

    admin = User.query.filter_by(role="admin").first()
    admin_email = current_app.config.get("ADMIN_EMAIL", "admin@placement.com")

    if admin:
        send_email(admin_email, "Monthly Placement Activity Report", html, html=True)

    return {
        "drives_conducted": drives_conducted,
        "applied": total_applied,
        "selected": total_selected
    }
