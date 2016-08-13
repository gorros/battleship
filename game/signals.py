from . import models

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def pre_save_handler(sender, instance, *args, **kwargs):
    if sender == models.Ship and not instance.health:
        instance.health = instance.category
    instance.full_clean()