"""clinic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Define the URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # URL pattern for the admin site
    path('', include("booking.urls")),  # Include URL patterns from the booking app
    path('user/', include("members.urls")),  # Include URL patterns from the members app
    path('pets/', include("pets.urls")),  # Include URL patterns from the pets app
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    """
    When in development mode (DEBUG=True), serve media files from the
    MEDIA_ROOT directory. This is necessary for handling user-uploaded content,
    such as images or files, during development. In production, serving
    media files is typically managed by the web server.
    """