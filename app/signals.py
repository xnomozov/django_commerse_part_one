from django.core.mail import send_mail

from config import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import json
import os

from app.models import Product, Customers


@receiver(pre_delete, sender=Product)
def product_pre_delete(sender, instance, **kwargs):
    file_path = os.path.join('app/deleted/products', f'{instance.id}_{instance.name}')
    data = {
        'id': instance.id,
        'name': instance.name,
        'price': instance.price,
        'rating': instance.rating,
        'description': instance.description,
        'discount': instance.discount,
        'quantity': instance.quantity,

    }
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


@receiver(pre_delete, sender=Customers)
def customers_pre_delete(sender, instance, **kwargs):
    directory = 'app/deleted/customers'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f'{instance.name}_id_{instance.id}')
    data = {
        'id': instance.id,
        'name': instance.name,
        'joined': str(instance.joined),
        'phone': instance.phone,
        'email': instance.email,
        'address': instance.billing_address,
        'is_active': instance.is_active,
    }

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        raise e


@receiver(post_save, sender=Customers)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        subject = f'Hi {instance.name}'
        message = 'Your account has been added and saved successfully as customer. Thank you! '
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [instance.email]
        try:
            send_mail(subject, message, email_from, email_to, fail_silently=False)
            print(f'Email sent to {instance.email}')
        except Exception as e:
            raise f'Error sending email: {str(e)}'
