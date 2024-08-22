from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Region, District, Service, Booking, Notification, Review, \
    Restaurant, Table, Payment, Worker, Location, Article, SupportTicket, SupportResponse, BonusPoint, Cashback, \
    ServiceUsageStatistic
from .serializers import RegionSerializer, DistrictSerializer, ServiceSerializer, BookingSerializer \
    , NotificationSerializer, ReviewSerializer, RestaurantSerializer, TableSerializer, PaymentSerializer, \
    WorkerSerializer, LocationSerializer, ArticleSerializer, SupportTicketSerializer, SupportResponseSerializer, \
    BonusPointSerializer, CashbackSerializer, ServiceUsageStatisticSerializer
from rest_framework import status, permissions
from django.utils import timezone
import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ServiceFilter, WorkerFilter, RestaurantFilter
from django.http import HttpResponse


class RegionListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)


class DistrictListAPIView(APIView):
    def get(self, request, region_id, *args, **kwargs):
        districts = District.objects.filter(region_id=region_id)
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)


class ServiceListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        services = Service.objects.filter(subscription=True)
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_class = ServiceFilter
        search_fields = ['name', 'description']
        ordering_fields = ['price', 'name']
        filterset = ServiceFilter(request.GET, queryset=services)
        filtered_services = filterset.qs
        serializer = ServiceSerializer(filtered_services, many=True)
        return Response(serializer.data)


class WorkerListAPIView(APIView):
    def get(self, request, service_id, *args, **kwargs):
        workers = Worker.objects.filter(service_id=service_id)
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_class = WorkerFilter
        search_fields = ['name', 'service__name']
        ordering_fields = ['price', 'name']
        filterset = WorkerFilter(request.GET, queryset=workers)
        filtered_workers = filterset.qs
        serializer = WorkerSerializer(filtered_workers, many=True)
        return Response(serializer.data)

    def post(self, request, service_id, *args, **kwargs):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(service_id=service_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class RestaurantListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.filter(subscription=True)
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_class = RestaurantFilter
        search_fields = ['name', 'description']
        ordering_fields = ['name']
        filterset = RestaurantFilter(request.GET, queryset=restaurants)
        filtered_restaurants = filterset.qs
        serializer = RestaurantSerializer(filtered_restaurants, many=True)
        return Response(serializer.data)


class TableListAPIView(APIView):
    def get(self, request, restaurant_id, *args, **kwargs):
        tables = Table.objects.filter(restaurant_id=restaurant_id, is_available=True)
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)


class BookingCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            worker = serializer.validated_data.get('worker', None)
            table = serializer.validated_data.get('table', None)
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']

            if worker:
                service = worker.service
                if date < timezone.now().date() or (date == timezone.now().date() and time <= timezone.now().time()):
                    return Response({'error': 'You cannot book a worker in the past.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                if Booking.objects.filter(worker=worker, date=date, time=time).exists():
                    return Response({'error': 'This worker is already booked for the selected time.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                booking = serializer.save(user=request.user, status='pending', advance_payment=worker.price * 0.5)
            elif table:
                if date < timezone.now().date() or (date == timezone.now().date() and time <= timezone.now().time()):
                    return Response({'error': 'You cannot book a table in the past.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                if Booking.objects.filter(table=table, date=date, time=time).exists():
                    return Response({'error': 'This table is already booked for the selected time.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                booking = serializer.save(user=request.user, status='pending',
                                          advance_payment=table.restaurant.price * 0.5)
            else:
                return Response({'error': 'Booking must be for either a worker or a table.'},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class PaymentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.validated_data['booking']
            amount = serializer.validated_data['amount']
            if booking.user != request.user:
                return Response({'error': 'You can only make a payment for your own bookings.'},
                                status=status.HTTP_400_BAD_REQUEST)

            payment = serializer.save(user=request.user, status='completed')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class ReviewCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.validated_data.get('service', None)
            restaurant = serializer.validated_data.get('restaurant', None)

            if service and not Booking.objects.filter(user=request.user, service=service).exists():
                return Response({'error': 'You can only leave a review after using the service.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if restaurant and not Booking.objects.filter(user=request.user, table__restaurant=restaurant).exists():
                return Response({'error': 'You can only leave a review after visiting the restaurant.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if not service and not restaurant:
                return Response({'error': 'Review must be for either a service or a restaurant.'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user=request.user)
            self.give_bonus_points(request.user, 10, "Review")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def give_bonus_points(self, user, points, reason):
        BonusPoint.objects.create(user=user, points=points, reason=reason)

    def give_cashback(self, user, amount, description):
        Cashback.objects.create(user=user, amount=amount, description=description)


class ReviewListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        service_id = request.query_params.get('service_id')
        restaurant_id = request.query_params.get('restaurant_id')

        if service_id:
            reviews = Review.objects.filter(service_id=service_id)
        elif restaurant_id:
            reviews = Review.objects.filter(restaurant_id=restaurant_id)
        else:
            return Response({'error': 'Service ID or Restaurant ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class BonusPointListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        bonus_points = BonusPoint.objects.filter(user=request.user)
        serializer = BonusPointSerializer(bonus_points, many=True)
        return Response(serializer.data)


class CashbackListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cashbacks = Cashback.objects.filter(user=request.user)
        serializer = CashbackSerializer(cashbacks, many=True)
        return Response(serializer.data)


class StatisticsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        bookings_count = Booking.objects.filter(user=user).count()
        reviews_count = Review.objects.filter(user=user).count()
        data = {
            'bookings_count': bookings_count,
            'reviews_count': reviews_count,
        }
        return Response(data)


class LocationCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)


logger = logging.getLogger('blog')


def my_view(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    return HttpResponse("Hello, world. You're at the my_view.")


class ArticleListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_subscriber():
            return Response({'error': 'Only admins and subscribed users can add articles.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, *args, **kwargs):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        article = self.get_object(pk)
        if not request.user.is_staff and request.user != article.author:
            return Response({'error': 'You do not have permission to edit this article.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        article = self.get_object(pk)
        if not request.user.is_staff and request.user != article.author:
            return Response({'error': 'You do not have permission to delete this article.'},
                            status=status.HTTP_403_FORBIDDEN)

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PopularServiceListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        services = Service.objects.order_by('-views_count')[:10]  # Eng ommabop 10 xizmat
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class PopularRestaurantListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.order_by('-views_count')[:10]  # Eng ommabop 10 restoran
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)


class ServiceDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, *args, **kwargs):
        service = self.get_object(pk)
        service.views_count += 1
        service.save()
        serializer = ServiceSerializer(service)
        return Response(serializer.data)


class RestaurantDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, *args, **kwargs):
        restaurant = self.get_object(pk)
        restaurant.views_count += 1
        restaurant.save()
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)


class SupportTicketListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tickets = SupportTicket.objects.filter(user=request.user)
        serializer = SupportTicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SupportTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupportTicketDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return SupportTicket.objects.get(pk=pk)
        except SupportTicket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, *args, **kwargs):
        ticket = self.get_object(pk)
        serializer = SupportTicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        ticket = self.get_object(pk)
        if ticket.user != request.user:
            return Response({'error': 'You do not have permission to edit this ticket.'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = SupportTicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        ticket = self.get_object(pk)
        if ticket.user != request.user:
            return Response({'error': 'You do not have permission to delete this ticket.'},
                            status=status.HTTP_403_FORBIDDEN)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SupportResponseCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, ticket_id, *args, **kwargs):
        try:
            ticket = SupportTicket.objects.get(pk=ticket_id)
        except SupportTicket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SupportResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ticket=ticket, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceUsageStatisticAPIView(APIView):
    def get(self, request, *args, **kwargs):
        statistics = ServiceUsageStatistic.objects.all()
        serializer = ServiceUsageStatisticSerializer(statistics, many=True)
        return Response(serializer.data)
