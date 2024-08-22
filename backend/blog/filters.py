import django_filters
from .models import Service, Worker, Restaurant


class ServiceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    region = django_filters.CharFilter(field_name="region__name", lookup_expr='icontains')
    district = django_filters.CharFilter(field_name="district__name", lookup_expr='icontains')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Service
        fields = ['min_price', 'max_price', 'region', 'district', 'name']


class WorkerFilter(django_filters.FilterSet):
    service = django_filters.CharFilter(field_name="service__name", lookup_expr='icontains')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Worker
        fields = ['service', 'name']


class RestaurantFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(field_name="region__name", lookup_expr='icontains')
    district = django_filters.CharFilter(field_name="district__name", lookup_expr='icontains')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Restaurant
        fields = ['region', 'district', 'name']
