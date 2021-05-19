from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created: bool, **kwargs):
    """Creates new profile when user signs up."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def update_profile(sender, instance, created: bool, **kwargs):
    """Updates user's profile."""
    if not created:
        instance.profile.save()
