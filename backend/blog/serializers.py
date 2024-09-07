from rest_framework import serializers
<<<<<<< HEAD
from .models import Region, District, Service, Worker, Booking, Table, Restaurant, Notification
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)
=======
from .models import Region, District, Service, Booking, Notification \
    , Review, Restaurant, Table, Payment, Worker, Location, Article, SupportTicket, SupportResponse, BonusPoint, \
    Cashback, ServiceUsageStatistic
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
<<<<<<< HEAD
        fields = ['id', 'name']
        read_only_fields = ['id']


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = District
        fields = ['id', 'name', 'region']
        read_only_fields = ['id']


class ServiceSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    district = DistrictSerializer()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'image', 'region', 'district', 'price', 'subscription', 'views_count']
        read_only_fields = ['id', 'views_count']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be positive.")
        return value


class WorkerSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = Worker
        fields = ['id', 'name', 'photo', 'available_from', 'available_to', 'price', 'service']
        read_only_fields = ['id']

    def validate_available_from(self, value):
        if value >= self.initial_data.get('available_to'):
            raise serializers.ValidationError("Available from time must be earlier than available to time.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be positive.")
        return value


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'read']
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        if not data.get('message'):
            raise serializers.ValidationError("Message field cannot be empty.")
        return data


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'image', 'region', 'district', 'subscription', 'views_count']
        read_only_fields = ['views_count']

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError("Restaurant name is required.")
        if not data.get('description'):
            raise serializers.ValidationError("Restaurant description is required.")
        return data


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'restaurant', 'number', 'image', 'is_available']

    def validate(self, data):
        if not data.get('restaurant'):
            raise serializers.ValidationError("Restaurant field is required.")
        if not data.get('number'):
            raise serializers.ValidationError("Table number is required.")
        return data
=======
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
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'service', 'table', 'date', 'time', 'advance_payment', 'status']
<<<<<<< HEAD
        read_only_fields = ['user', 'advance_payment', 'status']

    def validate(self, data):
        service = data.get('service')
        table = data.get('table')
        if not service and not table:
            raise serializers.ValidationError("Booking must be for either a service or a table.")
        if service and table:
            raise serializers.ValidationError("Booking cannot be for both a service and a table.")
        return data


logger = logging.getLogger(__name__)

=======
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
<<<<<<< HEAD
        fields = '__all__'

    def create(self, validated_data):
        logger.info(f"Notification created for user: {validated_data['user']}")
        return super().create(validated_data)

=======
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
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
<<<<<<< HEAD
        fields = '__all__'

    def validate_name(self, value):
        if Restaurant.objects.filter(name__iexact=value).exists():
            logger.warning(f"Restaurant with name {value} already exists.")
            raise serializers.ValidationError("This restaurant name already exists.")
        return value

    def create(self, validated_data):
        logger.info(f"Restaurant created with name: {validated_data['name']}")
        return super().create(validated_data)

=======
        fields = ['id', 'name', 'description', 'image', 'region', 'district', 'subscription', 'views_count']
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
<<<<<<< HEAD
        fields = '__all__'

    def validate_number(self, value):
        if Table.objects.filter(restaurant=self.context['restaurant'], number=value).exists():
            logger.warning(f"Table {value} already exists in restaurant {self.context['restaurant'].name}.")
            raise serializers.ValidationError("This table number already exists in this restaurant.")
        return value

    def create(self, validated_data):
        logger.info(f"Table {validated_data['number']} created for restaurant: {validated_data['restaurant'].name}")
        return super().create(validated_data)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        if data['service'] and Booking.objects.filter(service=data['service'], date=data['date'],
                                                      time=data['time']).exists():
            logger.warning(f"Service {data['service'].name} is already booked for {data['date']} at {data['time']}.")
            raise serializers.ValidationError("This service is already booked for the selected time.")

        if data['table'] and Booking.objects.filter(table=data['table'], date=data['date'], time=data['time']).exists():
            logger.warning(
                f"Table {data['table'].number} in restaurant {data['table'].restaurant.name} is already booked for {data['date']} at {data['time']}.")
            raise serializers.ValidationError("This table is already booked for the selected time.")

        if data['date'] < timezone.now().date() or (
                data['date'] == timezone.now().date() and data['time'] <= timezone.now().time()):
            logger.warning("Booking attempted in the past.")
            raise serializers.ValidationError("You cannot book a service or table in the past.")

        return data

    def create(self, validated_data):
        logger.info(f"Booking created for user: {validated_data['user'].name}")
        return super().create(validated_data)
=======
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
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6
