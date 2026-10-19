from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'event_name',
        'category',
        'event_date',
        'start_time',
        'location',
        'organizer',
        'ticket_price',
        'is_active',
    )

    list_filter=(
        'category',
        'event_date',
        'is_active',
    )

    search_fields = (
        'event_name',
        'location',
        'organizer',
    )
    

