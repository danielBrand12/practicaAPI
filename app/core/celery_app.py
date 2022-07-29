import os
import time
from celery import Celery

celery_app = Celery("celery")
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")


@celery_app.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True