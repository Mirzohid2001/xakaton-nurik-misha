from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Subscription
from rest_framework_simplejwt.tokens import RefreshToken

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        refresh = RefreshToken.for_user(instance)


@receiver(post_save, sender=Subscription)
def update_subscription_status(sender, instance, **kwargs):
    if not instance.is_valid():
        instance.is_active = False
        instance.save()