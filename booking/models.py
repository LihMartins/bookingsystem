"""
Models module for the booking app.

This module defines the database models used for handling service appointments.
It includes the `Appointment` model, which allows users to book services at
specified times and dates. The module also provides constants for service types
and available appointment times.
"""

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Constants defining service choices.
SERVICE_CHOICES = (
    ("Doctor care", "Doctor care"),
    ("Pet care", "Pet care"),
    ("Medical services", "Medical services"),
)

# Constants defining time choices for appointments.
TIME_CHOICES = (
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)


class Appointment(models.Model):
    """
    Represents an appointment for a service.

    Attributes:
        user (ForeignKey): The user associated with the appointment.
        service (CharField): The type of service requested, chosen from
            SERVICE_CHOICES.
        day (DateField): The date of the appointment.
        time (CharField): The time of the appointment, chosen from
            TIME_CHOICES.
        time_ordered (DateTimeField): The timestamp when the appointment
            was created.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    service = models.CharField(
        max_length=50, choices=SERVICE_CHOICES, default="Doctor care"
    )
    day = models.DateField(default=datetime.now)
    time = models.CharField(
        max_length=10, choices=TIME_CHOICES, default="3 PM"
    )
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        """
        Return a string representation of the appointment.

        This includes the user's username, the appointment day, and time.

        Returns:
            str: A string showing the user's username, appointment date,
            and time.
        """
        return f"{self.user.username} | day: {self.day} | time: {self.time}"
