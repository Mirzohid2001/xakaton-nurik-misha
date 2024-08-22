from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    social_links = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_subscriber(self):
        from django.utils import timezone
        current_date = timezone.now().date()
        return self.subscriptions.filter(start_date__lte=current_date, end_date__gte=current_date,
                                         is_active=True).exists()

class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than start date")
        super().save(*args, **kwargs)

    def is_valid(self):
        from django.utils import timezone
        return self.start_date <= timezone.now().date() <= self.end_date and self.is_active



