"""
This module defines the user registration form for the booking system.

It extends Django's built-in `UserCreationForm` to include additional
fields such as email, first name, and last name, and customizes the appearance
of these fields using Bootstrap classes for a more user-friendly interface.

Classes:
- RegisterUserForm: A form for creating a new user with additional fields for
email, first name, and last name, and custom widgets for enhanced styling.
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    """
    A form for registering a new user, extending `UserCreationForm`.

    This form adds fields for email, first name, and last name to the standard
    user creation form, with custom widgets that apply Bootstrap styling for
    a consistent and modern look.

    Attributes:
        email (EmailField): The user's email address.
        first_name (CharField): The user's first name.
        last_name (CharField): The user's last name.
    """

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'example@gmail.com'
                }
        )
    )
    first_name = forms.CharField(
        label='First Name',
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg'}
        )
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg'}
        )
    )

    class Meta:
        """

        Metadata for the RegisterUserForm class.

        Specifies the model to be used (User) and the fields to include in
        the form. It also defines the widgets to be used for rendering form
        fields with specific CSS classes.
        """

        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'password1', 'password2'
            )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and apply Bootstrap classes to each field.

        This method customizes the form's initialization by adding
        Bootstrap classes to the username, password1, and password2 fields
        for consistent styling.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = (
            'form-control form-control-lg'
        )
        self.fields['password1'].widget.attrs['class'] = (
            'form-control form-control-lg'
        )
        self.fields['password2'].widget.attrs['class'] = (
            'form-control form-control-lg'
        )
