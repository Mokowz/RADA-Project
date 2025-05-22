from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery('core')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-preds-daily-midnight': {
        'task': 'common.prediction.predict_all',
        'schedule': crontab(hour=0, minute=0, day_of_week=[0,1,2,3])
        # 'schedule': crontab(hour='*/3', minute=0)
    }
}
