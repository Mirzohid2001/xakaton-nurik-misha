import django_filters
from .models import Service, Worker, Restaurant


class ServiceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte', label='Max Price')
    region = django_filters.CharFilter(field_name="region__name", lookup_expr='icontains', label='Region')
    district = django_filters.CharFilter(field_name="district__name", lookup_expr='icontains', label='District')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains', label='Service Name')
    description = django_filters.CharFilter(field_name="description", lookup_expr='icontains', label='Description')
    subscription = django_filters.BooleanFilter(field_name="subscription", label='Subscription')

    class Meta:
        model = Service
        fields = ['min_price', 'max_price', 'region', 'district', 'name', 'description', 'subscription']


class WorkerFilter(django_filters.FilterSet):
    service = django_filters.CharFilter(field_name="service__name", lookup_expr='icontains', label='Service')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains', label='Worker Name')
    available_from = django_filters.TimeFilter(field_name="available_from", lookup_expr='gte', label='Available From')
    available_to = django_filters.TimeFilter(field_name="available_to", lookup_expr='lte', label='Available To')
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte', label='Min Price')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte', label='Max Price')

    class Meta:
        model = Worker
        fields = ['service', 'name', 'available_from', 'available_to', 'price_min', 'price_max']


class RestaurantFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(field_name="region__name", lookup_expr='icontains', label='Region')
    district = django_filters.CharFilter(field_name="district__name", lookup_expr='icontains', label='District')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains', label='Restaurant Name')
    description = django_filters.CharFilter(field_name="description", lookup_expr='icontains', label='Description')
    subscription = django_filters.BooleanFilter(field_name="subscription", label='Subscription')
    min_views_count = django_filters.NumberFilter(field_name="views_count", lookup_expr='gte', label='Min Views Count')
    max_views_count = django_filters.NumberFilter(field_name="views_count", lookup_expr='lte', label='Max Views Count')

    class Meta:
        model = Restaurant
        fields = ['region', 'district', 'name', 'description', 'subscription', 'min_views_count', 'max_views_count']
