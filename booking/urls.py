from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tickets/', views.list_tickets, name='list_tickets'),
    path('book/<int:ticket_id>/', views.book_ticket, name='book_ticket'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('tours/', views.list_tours, name='list_tours'),
    path('book_tour/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('tour/cancel/<int:tour_booking_id>/', views.cancel_tour, name='cancel_tour'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
]
