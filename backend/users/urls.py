from django.urls import path
from .views import UserRegistrationAPIView, UserProfileAPIView,SubscriptionCreateAPIView,SubscriptionListAPIView
urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(),name='register'),
    path('profile/', UserProfileAPIView.as_view(),name='profile'),
    path('subscription/create/', SubscriptionCreateAPIView.as_view(),name='subscription-create'),
    path('subscription/list/', SubscriptionListAPIView.as_view(),name='subscription-list'),
]