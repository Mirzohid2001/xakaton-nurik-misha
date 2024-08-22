from django.contrib import admin
from .models import (Region, District, Service, Worker, Restaurant, Table, Booking, PaymentMethod, Payment, Review,
                     BonusPoint, Location, Article, SupportTicket, SupportResponse, Cashback, ServiceUsageStatistic,
                     ServiceSearchFilter, RestaurantSearchFilter, RealTimeNotification, UserActivityStatistic,
                     AverageRating, UserProfileSetting, Offer, ChatMessage, SubscriptionReminder, ProgressTracker,
                     UserRole, PWAConfig, AnalyticsConfig, APILog, EmailLog, SEOConfig, ProductLog, UserInterest,
                     ReviewIncentive, Advertisement, Sponsorship)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region__name')
    list_filter = ('region',)
    ordering = ('region', 'name')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'district', 'price', 'subscription', 'views_count')
    search_fields = ('name', 'region__name', 'district__name', 'description')
    list_filter = ('region', 'district', 'subscription')
    ordering = ('name', 'price')


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'available_from', 'available_to', 'price')
    search_fields = ('name', 'service__name')
    list_filter = ('service',)
    ordering = ('service', 'name')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'district', 'subscription', 'views_count')
    search_fields = ('name', 'region__name', 'district__name', 'description')
    list_filter = ('region', 'district', 'subscription')
    ordering = ('name',)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'number', 'is_available')
    search_fields = ('restaurant__name',)
    list_filter = ('restaurant', 'is_available')
    ordering = ('restaurant', 'number')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'table', 'date', 'time', 'advance_payment', 'status')
    search_fields = ('user__name', 'service__name', 'table__restaurant__name')
    list_filter = ('status', 'date', 'service', 'table')
    ordering = ('-date', 'time')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'is_active')
    search_fields = ('name', 'provider')
    list_filter = ('is_active',)
    ordering = ('name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'amount', 'payment_method', 'status', 'created_at')
    search_fields = ('user__name', 'booking__service__name', 'payment_method__name', 'transaction_id')
    list_filter = ('status', 'payment_method', 'created_at')
    ordering = ('-created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'restaurant', 'rating', 'created_at')
    search_fields = ('user__name', 'service__name', 'restaurant__name', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)


@admin.register(BonusPoint)
class BonusPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'reason', 'created_at')
    search_fields = ('user__name', 'reason')
    ordering = ('-created_at',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude', 'timestamp')
    search_fields = ('user__username',)
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author__name', 'content')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subject', 'status', 'created_at', 'updated_at')
    search_fields = ('user__name', 'subject', 'description')
    list_filter = ('category', 'status', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(SupportResponse)
class SupportResponseAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'message', 'created_at')
    search_fields = ('ticket__subject', 'user__name', 'message')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Cashback)
class CashbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'description', 'created_at')
    search_fields = ('user__name', 'description')
    ordering = ('-created_at',)


@admin.register(ServiceUsageStatistic)
class ServiceUsageStatisticAdmin(admin.ModelAdmin):
    list_display = ('service', 'date', 'usage_count')
    search_fields = ('service__name',)
    list_filter = ('date',)
    ordering = ('-date',)


@admin.register(ServiceSearchFilter)
class ServiceSearchFilterAdmin(admin.ModelAdmin):
    list_display = ('service', 'query', 'date')
    search_fields = ('service__name', 'query')
    list_filter = ('date',)
    ordering = ('-date',)


@admin.register(RestaurantSearchFilter)
class RestaurantSearchFilterAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'query', 'date')
    search_fields = ('restaurant__name', 'query')
    list_filter = ('date',)
    ordering = ('-date',)


@admin.register(RealTimeNotification)
class RealTimeNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'read')
    search_fields = ('user__username', 'message')
    list_filter = ('read', 'created_at')
    ordering = ('-created_at',)


@admin.register(UserActivityStatistic)
class UserActivityStatisticAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'date', 'count')
    search_fields = ('user__username', 'activity_type')
    list_filter = ('activity_type', 'date')
    ordering = ('-date',)


@admin.register(AverageRating)
class AverageRatingAdmin(admin.ModelAdmin):
    list_display = ('service', 'restaurant', 'average_rating')
    search_fields = ('service__name', 'restaurant__name')
    ordering = ('-average_rating',)


@admin.register(UserProfileSetting)
class UserProfileSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'notifications_enabled', 'privacy_settings')
    search_fields = ('user__username', 'privacy_settings')
    list_filter = ('notifications_enabled',)
    ordering = ('user',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'restaurant', 'start_date', 'end_date', 'promo_code', 'discount_percentage')
    search_fields = ('title', 'service__name', 'restaurant__name', 'promo_code')
    list_filter = ('start_date', 'end_date', 'service', 'restaurant')
    ordering = ('-start_date',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'sent_at')
    search_fields = ('sender__username', 'receiver__username', 'message')
    list_filter = ('sent_at',)
    ordering = ('-sent_at',)


@admin.register(SubscriptionReminder)
class SubscriptionReminderAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'reminder_date')
    search_fields = ('subscription__user__username',)
    list_filter = ('reminder_date',)
    ordering = ('-reminder_date',)


@admin.register(ProgressTracker)
class ProgressTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'restaurant', 'progress_percentage')
    search_fields = ('user__username', 'service__name', 'restaurant__name')
    ordering = ('-progress_percentage',)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role__name')
    ordering = ('role', 'user')


@admin.register(PWAConfig)
class PWAConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'start_url', 'background_color', 'theme_color', 'display')
    search_fields = ('name', 'short_name', 'start_url')
    ordering = ('name',)


@admin.register(AnalyticsConfig)
class AnalyticsConfigAdmin(admin.ModelAdmin):
    list_display = ('provider', 'tracking_id', 'is_active')
    search_fields = ('provider', 'tracking_id')
    list_filter = ('provider', 'is_active')
    ordering = ('provider',)


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ('user', 'endpoint', 'method', 'status_code', 'request_time')
    search_fields = ('user__username', 'endpoint', 'method')
    list_filter = ('status_code', 'request_time')
    ordering = ('-request_time',)


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'sent_at', 'status')
    search_fields = ('user__username', 'subject', 'body')
    list_filter = ('status', 'sent_at')
    ordering = ('-sent_at',)


@admin.register(SEOConfig)
class SEOConfigAdmin(admin.ModelAdmin):
    list_display = ('page', 'title', 'description', 'keywords')
    search_fields = ('page', 'title', 'description', 'keywords')
    ordering = ('page',)


@admin.register(ProductLog)
class ProductLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'action', 'timestamp')
    search_fields = ('user__username', 'product', 'action')
    list_filter = ('action', 'timestamp')
    ordering = ('-timestamp',)


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'interest', 'created_at')
    search_fields = ('user__username', 'interest')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(ReviewIncentive)
class ReviewIncentiveAdmin(admin.ModelAdmin):
    list_display = ('review', 'bonus_points', 'discount_given')
    search_fields = ('review__id', 'review__user__name')
    list_filter = ('discount_given',)
    ordering = ('-bonus_points',)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    search_fields = ('title', 'url')
    list_filter = ('is_active', 'start_date', 'end_date')
    ordering = ('-start_date',)


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    search_fields = ('name', 'url')
    list_filter = ('is_active', 'start_date', 'end_date')
    ordering = ('-start_date',)
