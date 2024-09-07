from django.db.models.signals import post_save
from django.dispatch import receiver
<<<<<<< HEAD
from .models import User,Subscription
=======
from .models import User
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6
from rest_framework_simplejwt.tokens import RefreshToken

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        refresh = RefreshToken.for_user(instance)
<<<<<<< HEAD


@receiver(post_save, sender=Subscription)
def update_subscription_status(sender, instance, **kwargs):
    if not instance.is_valid():
        instance.is_active = False
        instance.save()
=======
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6
