from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    """
    Form for creating and updating Pet instances.
    """
    class Meta:
        model = Pet
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'profile_photo']
