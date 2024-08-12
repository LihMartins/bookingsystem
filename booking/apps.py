"""
This module configures the 'booking' application within the Django project.

It defines the configuration class that sets specific settings
for the application, such as the default primary key field type
and the application name. This configuration is essential
for properly initializing and managing the 'booking' app
within the larger Django project.
"""

from django.apps import AppConfig


class BookingConfig(AppConfig):
    """
    Configuration class for the 'booking' application.

    This class inherits from Django's AppConfig and is used to configure
    specific settings for the 'booking' application. It sets the default
    primary key field type to BigAutoField and defines the application
    name as 'booking'.

    Attributes:
        default_auto_field (str): Specifies the default type of primary key
        field for models in the application.
        name (str): The name of the application being configured.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking'
