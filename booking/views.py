from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Ticket, Booking, Tour, TourBooking, Traveler, UserProfile
from .forms import RegisterForm

def home(request):
    """Render the home page."""
    return render(request, 'booking/home.html')

def list_tickets(request):
    """List available tickets that have not yet departed and have available capacity."""
    tickets = Ticket.objects.filter(departure_datetime__gt=timezone.now()).filter(capacity__gt=0)
    return render(request, 'booking/list_tickets.html', {'tickets': tickets})

def book_ticket(request, ticket_id):
    """Book a ticket if available."""
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in or register to book a ticket.')
        return redirect('login')

    ticket = get_object_or_404(Ticket, id=ticket_id)
    profile = request.user.profile
    if request.method == 'POST':
        if profile.credit >= ticket.price:
            booking = Booking.objects.create(ticket=ticket, user=request.user, seat_number=Booking.objects.filter(ticket=ticket).count() + 1)
            profile.credit -= ticket.price
            profile.save()
            return redirect('booking_detail', booking_id=booking.id)
        else:
            messages.error(request, 'Insufficient credit to book this ticket.')
            return redirect('list_tickets')
    return render(request, 'booking/book_ticket.html', {'ticket': ticket})

def booking_detail(request, booking_id):
    """View details of a specific booking."""
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking/booking_detail.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user != booking.user and not request.user.is_superuser:
        return HttpResponseNotAllowed('You are not allowed to cancel this booking.')

    if request.method == 'POST':
        booking.cancel_booking()  # Process cancellation and refund
        return redirect('booking_detail', booking_id=booking.id)
    else:
        return render(request, 'booking/cancel_booking.html', {'booking': booking})

def list_tours(request):
    """List all available tours."""
    tours = Tour.objects.all()
    return render(request, 'booking/list_tours.html', {'tours': tours})

def book_tour(request, tour_id):
    """Book a tour if available."""
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in or register to book a tour.')
        return redirect('login')

    tour = get_object_or_404(Tour, id=tour_id)
    if tour.capacity <= TourBooking.objects.filter(tour=tour, is_cancelled=False).count():
        return HttpResponse("This tour is fully booked.", status=404)
    if request.method == 'POST':
        TourBooking.objects.create(tour=tour, traveler=request.user.traveler)
        return redirect('tour_detail', tour_id=tour.id)
    return render(request, 'booking/book_tour.html', {'tour': tour})

def tour_detail(request, tour_id):
    """View details of a specific tour."""
    tour = get_object_or_404(Tour, id=tour_id)
    return render(request, 'booking/tour_detail.html', {'tour': tour})

@login_required
def cancel_tour(request, tour_booking_id):
    tour_booking = get_object_or_404(TourBooking, id=tour_booking_id)
    if request.user.traveler != tour_booking.traveler and not request.user.is_superuser:
        return HttpResponseNotAllowed('You are not allowed to cancel this tour.')

    if request.method == 'POST':
        tour_booking.cancel_tour()  # Process cancellation and refund
        return redirect('tour_detail', tour_id=tour_booking.tour.id)
    else:
        return render(request, 'booking/cancel_tour.html', {'tour_booking': tour_booking})

def register(request):
    """Register a new user and create a Traveler profile."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Traveler.objects.create(user=user)  # Create a Traveler profile
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'booking/register.html', {'form': form})

def user_login(request):
    """Log in a user."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'booking/login.html', {'error': 'Invalid username or password'})
    return render(request, 'booking/login.html')

@login_required
def view_profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/profile.html', {
        'user': request.user,
        'profile': request.user.profile,
        'bookings': bookings
    })
