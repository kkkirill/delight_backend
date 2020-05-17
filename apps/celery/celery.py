from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from delight.settings import REDIS_URL

app = Celery('delight', broker=f'{REDIS_URL[:-1]}0')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(packages=settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'aggregate_listen_info': {
        'task': 'aggregate_listen_info',
        'schedule': crontab(minute=0, hour=0)
    }
}
