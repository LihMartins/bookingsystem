"""
URL configuration for the pets app.

This module defines the URL patterns that route to specific views in the
pets app. It includes paths for registering a new pet and for listing all
pets owned by the logged-in user.

URL Patterns:
- 'register/': Directs to the view that handles pet registration
(register_pet).
- '': Directs to the view that displays a list of all pets owned by the
current user (pet_list).

Imports:
- path: A function from Django used to define URL patterns.
- views: The views module of the pets app, where the logic for handling
each URL is implemented.

Attributes:
    urlpatterns (list): A list of URL pattern objects that Django uses to
    match incoming web requests to the appropriate view.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_pet, name='register_pet'),
    path('', views.pet_list, name='pet_list'),
]
