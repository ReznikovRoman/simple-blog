from django.dispatch import receiver
from django.db.models.signals import (post_save, )
from django.contrib.auth.models import User

from . import models


########################################################################################################################


@receiver(post_save, sender=models.CustomUser)
def create_profile(sender, instance, created: bool, **kwargs):
    if created:
        models.Profile.objects.create(
            user=instance
        )
        print("Profile created!")


@receiver(post_save, sender=models.CustomUser)
def update_profile(sender, instance, created: bool, **kwargs):
    if not created:
        instance.profile.save()
        print("Profile updated!")








