# Travel Agency Booking System

## Overview

The Travel Agency Booking System is a web application built using Django. It allows users to book train and flight tickets, register for tours, and manage their bookings. This system includes user authentication and profile management.

## Features

- User Authentication (Login, Register, Logout)
- Book Train and Flight Tickets
- View and Register for Tours
- Manage Bookings
- Ticket Cancellation with Refund

## Database Schema

### Tables and Their Data Types

1. **User** (Django's default user model)
   - `username`: CharField
   - `password`: CharField
   - `email`: EmailField
   - `first_name`: CharField
   - `last_name`: CharField

2. **Ticket**
   - `id`: AutoField (Primary Key)
   - `number`: CharField
   - `type`: CharField (Choices: 'train', 'flight')
   - `origin`: CharField
   - `destination`: CharField
   - `departure_datetime`: DateTimeField
   - `arrival_datetime`: DateTimeField
   - `capacity`: IntegerField
   - `price`: DecimalField

3. **Tour**
   - `id`: AutoField (Primary Key)
   - `name`: CharField
   - `description`: TextField
   - `departure_date`: DateField
   - `return_date`: DateField
   - `accommodation_details`: TextField
   - `capacity`: IntegerField
   - `price`: DecimalField

4. **Booking**
   - `id`: AutoField (Primary Key)
   - `user`: ForeignKey(User, on_delete=CASCADE)
   - `ticket`: ForeignKey(Ticket, on_delete=CASCADE, null=True, blank=True)
   - `tour`: ForeignKey(Tour, on_delete=CASCADE, null=True, blank=True)
   - `booking_date`: DateTimeField (auto_now_add=True)
   - `canceled`: BooleanField (default=False)
   - `refund_amount`: DecimalField (null=True, blank=True)

### Relations

- **User** to **Booking**: One-to-Many (A user can have multiple bookings)
- **Ticket** to **Booking**: One-to-Many (A ticket can be booked multiple times)
- **Tour** to **Booking**: One-to-Many (A tour can be booked multiple times)

## Installation Instructions

### Prerequisites

- Python 3.x
- Django 3.x or later
- SQLite (comes bundled with Python)

### Steps to Install and Start Server

1. **Unzip the Project Directory**

   If you have a zipped directory, unzip it first and navigate to the project directory.

   ```bash
   unzip travelagency.zip
   cd travelagency
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Django**

   ```bash
   pip install django
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the Server**

   ```bash
   python manage.py runserver
   ```

6. **Access the Application**

   Open a web browser and navigate to `http://127.0.0.1:8000` to access the application.

## Usage

### Admin Panel

You can manage your data models using Django's admin panel. Access it at `http://127.0.0.1:8000/admin` and log in with the superuser credentials you created. If a superuser is not already created, use the following command:

```bash
python manage.py createsuperuser
```

### Static Files

Ensure your static files are correctly set up for development. In a production environment, you may need to run:

```bash
python manage.py collectstatic
```

### Sample Data

To add initial sample data for testing, you can use Django's shell:

```bash
python manage.py shell
```

Then, add the following commands:

```python
from booking.models import Ticket, Tour
from django.contrib.auth.models import User

# Create sample tickets
Ticket.objects.create(number='TKT001', type='train', origin='Tehran', destination='Mashhad', departure_datetime='2024-06-25 08:00', arrival_datetime='2024-06-25 14:00', capacity=100, price=50.00)
Ticket.objects.create(number='TKT002', type='flight', origin='Tehran', destination='Shiraz', departure_datetime='2024-06-25 10:00', arrival_datetime='2024-06-25 12:00', capacity=150, price=80.00)

# Create sample tours
Tour.objects.create(name='Cultural Tour', description='Explore the cultural heritage of Iran.', departure_date='2024-07-01', return_date='2024-07-07', accommodation_details='4-star hotel', capacity=30, price=500.00)
Tour.objects.create(name='Adventure Tour', description='An adventurous journey through the mountains.', departure_date='2024-08-01', return_date='2024-08-10', accommodation_details='Camping and guesthouses', capacity=20, price=700.00)
```

## File Structure

- `travelagency/`
  - `booking/`
    - `migrations/`
    - `static/`
    - `templates/`
      - `booking/`
        - `base.html`
        - `home.html`
        - `login.html`
        - `register.html`
        - `profile.html`
        - `list_tickets.html`
        - `list_tours.html`
        - `book_ticket.html`
        - `book_tour.html`
        - `cancel_booking.html`
    - `admin.py`
    - `apps.py`
    - `models.py`
    - `urls.py`
    - `views.py`
  - `travelagency/`
    - `settings.py`
    - `urls.py`
    - `wsgi.py`
  - `manage.py`

## License

None

---
