from celery import Celery
from core.config import settings

celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    include=['tasks']
)
