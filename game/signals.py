from . import models

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=models.Ship)
def create_profile_handler(sender, instance, created, **kwargs):
    if created:
        instance.health = instance.category
