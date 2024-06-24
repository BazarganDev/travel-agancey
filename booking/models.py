from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Ticket(models.Model):
    TYPE_CHOICES = [
        ('train', 'Train'),
        ('flight', 'Flight'),
    ]
    number = models.CharField(max_length=20, verbose_name="Flight/Train Number", default='UNKNOWN')
    vehicle_type = models.CharField(max_length=100, verbose_name="Type of Airplane/Train", default='UNKNOWN')
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.number} - {self.origin} to {self.destination}"

class Booking(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    booking_code = models.UUIDField(default=uuid.uuid4, editable=False)
    is_cancelled = models.BooleanField(default=False)
    refund_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)

    def cancel_booking(self):
        """Cancel the booking and calculate the refund."""
        if not self.is_cancelled:
            self.is_cancelled = True
            self.refund_amount = self.ticket.price * Decimal('0.8')  # 80% refund
            self.user.profile.credit += self.refund_amount  # Refund to user's credit
            self.user.profile.save()
            self.save()

class Traveler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Tour(models.Model):
    travel_date = models.DateField()
    return_date = models.DateField()
    accommodation_details = models.TextField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"Tour from {self.travel_date} to {self.return_date}"

class TourBooking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)
    refund_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    def cancel_tour(self):
        """Cancel the tour booking and calculate the refund."""
        if not self.is_cancelled:
            self.is_cancelled = True
            self.refund_amount = self.tour.price * 0.8  # 80% refund
            self.traveler.user.profile.credit += self.refund_amount  # Refund to user's credit
            self.traveler.user.profile.save()
            self.save()

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)  # $100 credit on signup

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
