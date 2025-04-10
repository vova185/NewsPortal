# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings
# from .models import PostCategory
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
#
# def send_notifications(preview, pk, title, subscribers_emails):
#     html_content = render_to_string(
#         'post_to_email.html',
#         {'text': preview, 'link': f"{settings.SITE_URL}/news/{pk}"})
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body="",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers_emails,
#     )
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         category = instance.categories.all()
#         subscribers_emails = []
#         for category in category:
#             subs = category.subscribers.all()
#             subscribers_emails += [s.email for s in subs]
#
#         subscribers_emails = set(subscribers_emails)
#
#         send_notifications(instance.content[:50], instance.id, instance.title, subscribers_emails)
