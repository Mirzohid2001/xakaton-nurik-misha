from django.db import models
from .models import User, Subscription

class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def by_email(self, email):
        return self.filter(email=email)


class SubscriptionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def valid(self):
        from django.utils import timezone
        current_date = timezone.now().date()
        return self.filter(start_date__lte=current_date, end_date__gte=current_date, is_active=True)
