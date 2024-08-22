from django.urls import path
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

