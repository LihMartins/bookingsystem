"""
This module defines the `Pet` model, representing a pet owned by a user in the system.

The `Pet` model includes attributes such as the owner's user reference, the pet's name,
birth date, gender, and an optional profile photo. This model serves as the foundation
for managing and displaying pet-related data within the application, allowing users
to register and maintain information about their pets.
"""

from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    """
    Represents a pet owned by a user.

    Attributes:
        owner (ForeignKey): Reference to the user who owns the pet.
        first_name (CharField): The first name of the pet.
        last_name (CharField): The last name of the pet.
        date_of_birth (DateField): The birth date of the pet.
        gender (CharField): The gender of the pet.
        profile_photo (ImageField): The profile photo of the pet.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_photo = models.ImageField(upload_to='pet_photos/', blank=True, null=True)

    def __str__(self):
        """
        Returns the string representation of the pet.

        Returns:
        str: The full name of the pet.
        """
        return f"{self.first_name} {self.last_name}"
