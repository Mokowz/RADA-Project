# from celery import Celery
from celery.schedules import crontab
from .prediction import predict_all, app

# app = Celery()

app.conf.beat_schedule = {
    'run-preds-daily-midnight': {
        'task': 'predict_all',
        'schedule': crontab(hour=0, minute=0, day_of_week=[0,1,2,3,4,5,6])
    }
}