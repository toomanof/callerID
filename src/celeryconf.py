import os

from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('caller')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    from src.base.tasks import update_registry

    schedule = crontab(hour=0, minute=0)
    sender.add_periodic_task(schedule, update_registry.s(), name='update registry')


