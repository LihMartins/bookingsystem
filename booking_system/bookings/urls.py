
"""
URL patterns for the bookings app.

This module defines the URL patterns specific to the bookings functionality,
including listing bookings and creating new bookings.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('create/', views.create_booking, name='create_booking'),
]