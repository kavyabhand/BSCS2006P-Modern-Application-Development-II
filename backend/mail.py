import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

def send_email(to, subject, body, html=False):
    user = current_app.config.get("SMTP_USER", "")
    password = current_app.config.get("SMTP_PASSWORD", "")

    if not user or not password:
        print(f"Email skipped (no SMTP config): {to} - {subject}")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = user
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html" if html else "plain"))

        host = current_app.config.get("SMTP_HOST", "smtp.gmail.com")
        port = current_app.config.get("SMTP_PORT", 587)

        with smtplib.SMTP(host, port, timeout=10) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)

        print(f"Email sent: {to} - {subject}")
        return True

    except Exception as e:
        print(f"Email failed (app continues): {to} - {subject} - {e}")
        return False
