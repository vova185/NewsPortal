import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf. broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.send_daily_post_to_email_task',
        'schedule': crontab(hour='8', minute='0', day_of_week='monday'),
    },
}

# app.conf.timezone = 'Asia/Yekaterinburg'