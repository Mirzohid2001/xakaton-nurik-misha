from rest_framework import serializers
from .models import Region, District, Service, Worker, Booking, Table, Restaurant, Notification
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
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


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'service', 'table', 'date', 'time', 'advance_payment', 'status']
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


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def create(self, validated_data):
        logger.info(f"Notification created for user: {validated_data['user']}")
        return super().create(validated_data)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

    def validate_name(self, value):
        if Restaurant.objects.filter(name__iexact=value).exists():
            logger.warning(f"Restaurant with name {value} already exists.")
            raise serializers.ValidationError("This restaurant name already exists.")
        return value

    def create(self, validated_data):
        logger.info(f"Restaurant created with name: {validated_data['name']}")
        return super().create(validated_data)


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
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
