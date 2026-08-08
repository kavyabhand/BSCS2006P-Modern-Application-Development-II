from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "ppa",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks.export", "tasks.reports", "tasks.reminders"]
)

celery.conf.beat_schedule = {
    "daily-reminders": {
        "task": "tasks.reminders.send_deadline_reminders",
        "schedule": crontab(hour=9, minute=0),
    },
    "monthly-report": {
        "task": "tasks.reports.generate_monthly_report",
        "schedule": crontab(day_of_month=1, hour=8, minute=0),
    },
}

def init_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
