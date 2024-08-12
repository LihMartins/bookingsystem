"""
URL patterns for the bookings app.

This module defines the URL patterns specific to the bookings functionality,
including listing bookings, creating new bookings, and managing user and staff
panels.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking', views.booking, name='booking'),
    path('booking-submit', views.booking_submit, name='booking_submit'),
    path('user-panel', views.user_panel, name='user_panel'),
    path('user-update/<int:id>', views.user_update, name='user_update'),
    path(
        'user-update-submit/<int:id>',
        views.user_update_submit,
        name='user_update_submit'
    ),
    path('staff-panel', views.staff_panel, name='staff_panel'),
]
