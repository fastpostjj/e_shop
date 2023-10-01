from django.contrib import admin

from user_auth.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'phone',
        'is_active'
        )
    list_display_links = (
        'id',
        'email',
        'phone'
        )
    list_filter = (
        'id',
        'email',
        'phone'
        )
    search_fields = (
        'id',
        'email',
        'phone',
        )
    
