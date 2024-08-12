"""
This module defines the URL patterns for the 'members' application.

It handles routes related to user authentication such as login,
logout, and registration.
"""

from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for user login
    path('login_user', views.login_user, name='login'),

    # URL pattern for user logout
    path('logout_user', views.logout_user, name='logout'),

    # URL pattern for user registration
    path('register_user', views.register_user, name='register'),
]
