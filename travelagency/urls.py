from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include('booking.urls')),
    path('', RedirectView.as_view(url='/booking/', permanent=True)),  # Redirect root to /booking/
]
