from . import models

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=models.Ship)
@receiver(pre_save, sender=models.Battle)
@receiver(pre_save, sender=models.Move)
def pre_save_handler(sender, instance, *args, **kwargs):
    instance.full_clean()