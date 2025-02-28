from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import *
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
import datetime

def send_post_to_email(preview, pk, title, subscribers_emails):
    html_content = render_to_string(
        'post_to_email.html',
        {'text': preview, 'link': f"{settings.SITE_URL}/news/{pk}"})

    msg = EmailMultiAlternatives(
        subject=title,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        category = instance.categories.all()
        subscribers_emails = []
        for category in category:
            subs = category.subscribers.all()
            subscribers_emails += [s.email for s in subs]
        subscribers_emails = set(subscribers_emails)

        send_post_to_email(instance.content[:50], instance.id, instance.title, subscribers_emails)

def send_daily_post_to_email():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    categories = set(posts.values_list('categories__all_category', flat=True))
    subscribers = set(Category.objects.filter(all_category__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Публикации за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

    send_daily_post_to_email()