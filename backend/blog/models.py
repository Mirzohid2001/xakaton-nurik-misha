from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, Subscription
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model


# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'


class District(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, related_name='districts', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    region = models.ForeignKey(Region, related_name='services', on_delete=models.CASCADE)
    district = models.ForeignKey(District, related_name='services', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subscription = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Worker(models.Model):
    service = models.ForeignKey(Service, related_name='workers', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='workers/', null=True, blank=True)
    available_from = models.TimeField()
    available_to = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.message}"


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurants/', null=True, blank=True)
    region = models.ForeignKey(Region, related_name='restaurants', on_delete=models.CASCADE)
    district = models.ForeignKey(District, related_name='restaurants', on_delete=models.CASCADE)
    subscription = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='tables', on_delete=models.CASCADE)
    number = models.IntegerField()
    image = models.ImageField(upload_to='tables/', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.restaurant.name} - Table {self.number}"


class Booking(models.Model):
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='bookings', on_delete=models.CASCADE, null=True, blank=True)
    table = models.ForeignKey(Table, related_name='bookings', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50,
                              choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        if self.service:
            return f"{self.user.name} - {self.service.name}"
        elif self.table:
            return f"{self.user.name} - {self.table.restaurant.name} - Table {self.table.number}"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'


class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, related_name='payments', on_delete=models.CASCADE)
    status = models.CharField(max_length=50,
                              choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.amount} - {self.payment_method.name} - {self.status}"


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'service', 'restaurant')


class BonusPoint(models.Model):
    user = models.ForeignKey(User, related_name='bonus_points', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.points} points for {self.reason}"


class Location(models.Model):
    user = models.ForeignKey(User, related_name='locations', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.latitude}, {self.longitude}"


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SupportTicket(models.Model):
    SERVICE = 'service'
    RESTAURANT = 'restaurant'
    CATEGORY_CHOICES = [
        (SERVICE, 'Service'),
        (RESTAURANT, 'Restaurant'),
    ]

    user = models.ForeignKey(User, related_name='support_tickets', on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    service = models.ForeignKey(Service, related_name='support_tickets', on_delete=models.CASCADE, null=True,
                                blank=True)
    restaurant = models.ForeignKey(Restaurant, related_name='support_tickets', on_delete=models.CASCADE, null=True,
                                   blank=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')

    def __str__(self):
        return self.subject


class SupportResponse(models.Model):
    ticket = models.ForeignKey(SupportTicket, related_name='responses', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='support_responses', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.ticket.subject} by {self.user.username}"


class Cashback(models.Model):
    user = models.ForeignKey(User, related_name='cashbacks', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.amount} cashback for {self.description}"


class ServiceUsageStatistic(models.Model):
    service = models.ForeignKey(Service, related_name='usage_statistics', on_delete=models.CASCADE)
    date = models.DateField()
    usage_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.service.name} - {self.date} - {self.usage_count} usages"


class ServiceSearchFilter(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search for {self.query} on {self.date}"


class RestaurantSearchFilter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search for {self.query} on {self.date}"


class RealTimeNotification(models.Model):
    user = models.ForeignKey(User, related_name='real_time_notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"


class UserActivityStatistic(models.Model):
    user = models.ForeignKey(User, related_name='activity_statistics', on_delete=models.CASCADE)
    date = models.DateField()
    activity_type = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"


class AverageRating(models.Model):
    service = models.ForeignKey(Service, related_name='average_ratings', on_delete=models.CASCADE, null=True,
                                blank=True)
    restaurant = models.ForeignKey(Restaurant, related_name='average_ratings', on_delete=models.CASCADE, null=True,
                                   blank=True)
    average_rating = models.FloatField()

    def __str__(self):
        if self.service:
            return f"Average Rating for Service: {self.service.name} - {self.average_rating}"
        elif self.restaurant:
            return f"Average Rating for Restaurant: {self.restaurant.name} - {self.average_rating}"


class UserProfileSetting(models.Model):
    user = models.OneToOneField(User, related_name='profile_settings', on_delete=models.CASCADE)
    preferred_services = models.ManyToManyField(Service, related_name='preferred_by_users', blank=True)
    preferred_restaurants = models.ManyToManyField(Restaurant, related_name='preferred_by_users', blank=True)
    notifications_enabled = models.BooleanField(default=True)
    privacy_settings = models.TextField(default="Public")

    def __str__(self):
        return f"Settings for {self.user.username}"


class Offer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    service = models.ForeignKey(Service, related_name='offers', on_delete=models.CASCADE, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, related_name='offers', on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    promo_code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        target = self.service if self.service else self.restaurant
        return f"Offer: {self.title} for {target.name}"


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class SubscriptionReminder(models.Model):
    subscription = models.OneToOneField(Subscription, related_name='reminder', on_delete=models.CASCADE)
    reminder_date = models.DateField()

    def __str__(self):
        return f"Reminder for subscription of {self.subscription.user.username} on {self.reminder_date}"


class ProgressTracker(models.Model):
    user = models.ForeignKey(User, related_name='progress_trackers', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='progress_trackers', on_delete=models.CASCADE, null=True,
                                blank=True)
    restaurant = models.ForeignKey(Restaurant, related_name='progress_trackers', on_delete=models.CASCADE, null=True,
                                   blank=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        target = self.service if self.service else self.restaurant
        return f"Progress for {self.user.username} in {target.name} - {self.progress_percentage}%"


User = get_user_model()


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


class PWAConfig(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)
    start_url = models.CharField(max_length=255)
    background_color = models.CharField(max_length=7)
    theme_color = models.CharField(max_length=7)
    display = models.CharField(max_length=20, choices=[('standalone', 'Standalone'), ('fullscreen', 'Fullscreen')])

    def __str__(self):
        return self.name


class AnalyticsConfig(models.Model):
    provider = models.CharField(max_length=50, choices=[('google', 'Google Analytics'), ('matomo', 'Matomo')])
    tracking_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider} - {self.tracking_id}"


class APILog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.endpoint} - {self.method} - {self.status_code}"


class EmailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('sent', 'Sent'), ('failed', 'Failed')])

    def __str__(self):
        return f"{self.user.username} - {self.subject} - {self.status}"


class SEOConfig(models.Model):
    page = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=255)

    def __str__(self):
        return f"SEO for {self.page}"


class ProductLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product} - {self.action} - {self.timestamp}"


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.interest}"


class ReviewIncentive(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    bonus_points = models.IntegerField(default=0)
    discount_given = models.BooleanField(default=False)

    def __str__(self):
        return f"Incentive for Review ID {self.review.id}"


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    url = models.URLField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Sponsorship(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='sponsors/', null=True, blank=True)
    url = models.URLField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
