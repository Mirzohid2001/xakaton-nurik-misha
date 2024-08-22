from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Subscription

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'phone_number', 'profile_picture', 'bio', 'social_links')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'email', 'phone_number'),
        }),
    )
    list_display = ('username', 'name', 'email', 'phone_number', 'is_active', 'is_staff')
    search_fields = ('username', 'name', 'email', 'phone_number')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    ordering = ('username',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'is_active')
    search_fields = ('user__username', 'user__name')
    list_filter = ('is_active', 'start_date', 'end_date')
    ordering = ('-start_date',)

