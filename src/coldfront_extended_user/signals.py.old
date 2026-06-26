# UserCustomFields/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserCustomFields

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_custom_fields(sender, instance, created, **kwargs):
    """
    Automatically creates a UserCustomFields object whenever a new User is created.
    """
    if created:
        UserCustomFields.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_custom_fields(sender, instance, **kwargs):
    """
    Ensures the custom fields object is saved if the user is saved.
    """
    if hasattr(instance, 'usercustomfields'):
        instance.usercustomfields.save()