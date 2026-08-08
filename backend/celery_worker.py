from app import app
from celery_app import celery
import tasks.export
import tasks.reports
import tasks.reminders

celery.conf.update(app.config)
