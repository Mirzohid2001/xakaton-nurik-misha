from django.db import models
from users.models import User, Subscription


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


class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
    status = models.CharField(max_length=50,
                              choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.amount} - {self.status}"


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
    service = models.ForeignKey('Service', related_name='support_tickets', on_delete=models.CASCADE, null=True,
                                blank=True)
    restaurant = models.ForeignKey('Restaurant', related_name='support_tickets', on_delete=models.CASCADE, null=True,
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
