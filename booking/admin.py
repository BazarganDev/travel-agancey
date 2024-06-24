from django.contrib import admin
from .models import Ticket, Booking, Tour, TourBooking, UserProfile

admin.site.register(Ticket)
admin.site.register(Booking)
admin.site.register(Tour)
admin.site.register(TourBooking)
admin.site.register(UserProfile)
