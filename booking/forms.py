"""
Forms module for the booking app.

This module defines a form used for handling user input related to booking
appointments. It uses Django's ModelForm to automatically generate form fields
based on the Booking model, allowing users to select a date, time, and provide
a description for their appointment.

Classes:
    BookingForm: A ModelForm that corresponds to the Booking model, providing
    fields for date, time, and description.

Attributes:
    Meta (class): Specifies the model to be used (Booking) and the fields to
    include in the form. Also defines the widgets to be used for rendering form
    fields with specific CSS classes.

Form Fields:
    - date: A DateInput field for selecting the appointment date, styled with
    Bootstrap's 'form-control' class.
    - time: A TimeInput field for selecting the appointment time, styled with
    Bootstrap's 'form-control' class.
    - description: A Textarea field for entering a description, styled with
    Bootstrap's 'form-control' class.
"""

from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    A form for creating or updating Booking instances.

    This form provides fields to allow users to input the date, time, and a
    description for their appointment. The form fields are styled using
    Bootstrap's 'form-control' class to ensure a consistent and user-friendly
    interface.
    """

    class Meta:
        """
        Metadata for the BookingForm class.

        Specifies the model to be used (Booking) and the fields to include in
        the form. It also defines the widgets to be used for rendering form
        fields with specific CSS classes.
        """

        model = Booking
        fields = ['date', 'time', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
