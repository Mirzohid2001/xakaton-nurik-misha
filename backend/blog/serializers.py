from rest_framework import serializers
from .models import Region, District, Service, Booking, Notification \
    , Review, Restaurant, Table, Payment, Worker, Location, Article, SupportTicket, SupportResponse, BonusPoint, \
    Cashback, ServiceUsageStatistic


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'region')

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'service', 'name', 'photo', 'available_from', 'available_to', 'price']

class ServiceSerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'image', 'region', 'district', 'price', 'subscription', 'workers', 'views_count']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'service', 'table', 'date', 'time', 'advance_payment', 'status']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'read']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'service', 'restaurant', 'rating', 'comment', 'created_at']
        extra_kwargs = {
            'rating': {'min_value': 1, 'max_value': 5}
        }

class BonusPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusPoint
        fields = ['id', 'user', 'points', 'reason', 'created_at']

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'image', 'region', 'district', 'subscription', 'views_count']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'restaurant', 'number', 'image', 'is_available']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'booking', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'user', 'latitude', 'longitude', 'timestamp']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']

class SupportResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportResponse
        fields = ['id', 'ticket', 'user', 'message', 'created_at']

class SupportTicketSerializer(serializers.ModelSerializer):
    responses = SupportResponseSerializer(many=True, read_only=True)

    class Meta:
        model = SupportTicket
        fields = ['id', 'user', 'category', 'service', 'restaurant', 'subject', 'description', 'created_at', 'updated_at', 'status', 'responses']

class CashbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashback
        fields = ['id', 'user', 'amount', 'description', 'created_at']

class ServiceUsageStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUsageStatistic
        fields = ['service', 'date', 'usage_count']