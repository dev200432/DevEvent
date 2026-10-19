from django.contrib import admin
from .models import Registration

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'event', 
        'registration_date', 
        'status',
        )
    list_filter = (
        'status', 
        'registration_date',
        )
    search_fields = (
        'user__username', 
        'event__event_name',
        )