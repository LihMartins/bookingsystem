"""
This module defines the form used for creating and updating Pet instances.

The form is based on Django's ModelForm, which automatically generates form
fields for the Pet model's attributes. This form is utilized within views
that handle pet registration and updates.
"""

from django import forms
from .models import Pet


class PetForm(forms.ModelForm):
    """
    Form for creating and updating Pet instances.

    This form provides fields for the first name, last name, date of birth,
    gender, and profile photo of a pet.

    Attributes:
        model (Pet): The Pet model is used to create or update instances.
        fields (list): Specifies the fields to include in the form.
    """

    class Meta:
        """
        Metadata for the PetForm class.

        Specifies the model to be used (Pet) and the fields to include in
        the form.
        """

        model = Pet
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'profile_photo'
        ]
