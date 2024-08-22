import logging
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Region, District, Service, Worker, Booking, Table, Restaurant, Notification
from .serializers import RegionSerializer, DistrictSerializer, ServiceSerializer, WorkerSerializer, NotificationSerializer, RestaurantSerializer, TableSerializer, BookingSerializer

logger = logging.getLogger(__name__)

class RegionListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        logger.info("Region list fetched")
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logger.info("Creating a new region")
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Region created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create region: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DistrictListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        logger.info("District list fetched")
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logger.info("Creating a new district")
        serializer = DistrictSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("District created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create district: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        logger.info("Service list fetched")
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logger.info("Creating a new service")
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Service created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create service: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        logger.info("Worker list fetched")
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logger.info("Creating a new worker")
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Worker created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create worker: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        logger.info(f"Fetched {notifications.count()} notifications for user {request.user.name}")
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.info(f"Notification created for user {request.user.name}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to create notification for user {request.user.name}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.filter(subscription=True)
        serializer = RestaurantSerializer(restaurants, many=True)
        logger.info("Fetched restaurant list")
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Restaurant {serializer.data['name']} created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to create restaurant: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableListCreateAPIView(APIView):
    def get(self, request, restaurant_id, *args, **kwargs):
        tables = Table.objects.filter(restaurant_id=restaurant_id, is_available=True)
        serializer = TableSerializer(tables, many=True)
        logger.info(f"Fetched table list for restaurant id {restaurant_id}")
        return Response(serializer.data)

    def post(self, request, restaurant_id, *args, **kwargs):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        serializer = TableSerializer(data=request.data, context={'restaurant': restaurant})
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Table {serializer.data['number']} created for restaurant {restaurant.name}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to create table for restaurant {restaurant.name}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.info(f"Booking created for user {request.user.name}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to create booking for user {request.user.name}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

