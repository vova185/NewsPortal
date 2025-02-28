from celery import shared_task
from .email import send_post_to_email, send_daily_post_to_email

@shared_task
def send_post_to_email_task():
    return send_post_to_email

@shared_task
def send_daily_post_to_email_task():
    return send_daily_post_to_email()
