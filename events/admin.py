from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'event_date', 'phone', 'email', 'created_at')
    list_filter = ('event_type', 'event_date')
    search_fields = ('name', 'email', 'phone') 