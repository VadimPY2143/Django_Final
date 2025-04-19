from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from Django import settings


@shared_task
def send_html_mail(plain_message, html_message, email):
    message = EmailMultiAlternatives(
        subject='Booking Confirmation',
        body=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()
