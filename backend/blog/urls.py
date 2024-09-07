from django.urls import path
<<<<<<< HEAD
from .views import (
    RegionListCreateAPIView,
    DistrictListCreateAPIView,
    ServiceListCreateAPIView,
    WorkerListCreateAPIView
)

urlpatterns = [
    path('regions/', RegionListCreateAPIView.as_view(), name='region-list-create'),
    path('districts/', DistrictListCreateAPIView.as_view(), name='district-list-create'),
    path('services/', ServiceListCreateAPIView.as_view(), name='service-list-create'),
    path('workers/', WorkerListCreateAPIView.as_view(), name='worker-list-create'),
]

=======
from .views import RegionListAPIView, DistrictListAPIView, ServiceListAPIView, BookingCreateAPIView, \
    NotificationListAPIView, NotificationCreateAPIView, ReviewListAPIView, ReviewCreateAPIView, WorkerListAPIView, \
    RestaurantListAPIView, TableListAPIView, LocationCreateAPIView, \
    StatisticsAPIView, ArticleListCreateAPIView, ArticleDetailAPIView, PopularRestaurantListAPIView, \
    PopularServiceListAPIView, \
    ServiceDetailAPIView, RestaurantDetailAPIView, SupportTicketDetailAPIView, SupportTicketListCreateAPIView, \
    SupportResponseCreateAPIView, BonusPointListAPIView, CashbackListAPIView, ServiceUsageStatisticAPIView

urlpatterns = [
    path('region/', RegionListAPIView.as_view(), name='region_list'),
    path('district/<int:region_id>/', DistrictListAPIView.as_view(), name='district_list'),
    path('service/<int:district_id>/', ServiceListAPIView.as_view(), name='service_list'),
    path('booking/', BookingCreateAPIView.as_view(), name='booking_create'),
    path('notification/', NotificationListAPIView.as_view(), name='notification_list'),
    path('notification/create/', NotificationCreateAPIView.as_view(), name='notification_create'),
    path('reviews/', ReviewListAPIView.as_view(), name='review_list'),
    path('reviews/create/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('bonus-points/', BonusPointListAPIView.as_view(), name='bonus_point_list'),
    path('cashbacks/', CashbackListAPIView.as_view(), name='cashback_list'),
    path('services/<int:service_id>/workers/', WorkerListAPIView.as_view(), name='workers_list'),
    path('restaurants/<int:district_id>/', RestaurantListAPIView.as_view(), name='restaurants_list'),
    path('tables/<int:restaurant_id>/', TableListAPIView.as_view(), name='tables_list'),
    path('location/create/', LocationCreateAPIView.as_view(), name='location_create'),
    path('statistics/', StatisticsAPIView.as_view(), name='statistics'),
    path('articles/', ArticleListCreateAPIView.as_view(), name='article_list_create'),
    path('articles/<int:pk>/', ArticleDetailAPIView.as_view(), name='article_detail'),
    path('popular-services/', PopularServiceListAPIView.as_view(), name='popular_service_list'),
    path('popular-restaurants/', PopularRestaurantListAPIView.as_view(), name='popular_restaurant_list'),
    path('services/<int:pk>/', ServiceDetailAPIView.as_view(), name='service_detail'),
    path('restaurants/<int:pk>/', RestaurantDetailAPIView.as_view(), name='restaurant_detail'),
    path('support-tickets/', SupportTicketListCreateAPIView.as_view(), name='support_ticket_list_create'),
    path('support-tickets/<int:pk>/', SupportTicketDetailAPIView.as_view(), name='support_ticket_detail'),
    path('support-tickets/<int:ticket_id>/responses/', SupportResponseCreateAPIView.as_view(),
         name='support_response_create'),
    path('usage-statistics/', ServiceUsageStatisticAPIView.as_view(), name='service_usage_statistics'),

]
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6
