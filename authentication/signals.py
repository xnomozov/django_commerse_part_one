from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import CustomUser
from config import settings


@receiver(post_save, sender=CustomUser)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        subject = f'Hi {instance.username}'
        message = 'Your account has been registered and saved successfully. Thank you! '
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [instance.email]
        try:
            send_mail(subject, message, email_from, email_to, fail_silently=False)
            print(f'Email sent to {instance.email}')
        except Exception as e:
            raise f'Error sending email: {str(e)}'




