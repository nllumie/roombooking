from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'room', 'start_time')
    search_fields = ('room__name', 'user__username')
    date_hierarchy = 'start_time'

