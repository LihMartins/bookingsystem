"""
This module configures the 'pets' application within the Django project.

It defines the configuration class that sets specific settings for the
application, such as the default primary key field type and the application
name. This configuration is essential for properly initializing and managing
the 'pets' app within the larger Django project.
"""

from django.apps import AppConfig


class PetsConfig(AppConfig):
    """
    Configuration class for the 'pets' application.

    This class is used to configure the 'pets' application within the Django
    project. It specifies the default primary key field type for models and
    the application name.

    Attributes:
        default_auto_field (str): Specifies the default type of primary key
            field for models in the application.
        name (str): The name of the application being configured.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pets'
