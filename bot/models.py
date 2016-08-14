from django.db import models
from django.utils.functional import cached_property


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FBUser(TimeStampedModel):
    fb_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        ordering = ["-created"]
        verbose_name = "facebook user"
        verbose_name_plural = "facebook users"

    @cached_property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)
