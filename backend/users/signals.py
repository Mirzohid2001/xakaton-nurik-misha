from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        refresh = RefreshToken.for_user(instance)
