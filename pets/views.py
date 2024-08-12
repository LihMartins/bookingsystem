"""
This module provides views for managing pet registration.

Also listing within the application.

The `register_pet` view handles the form submission for adding new pets,
ensuring that only authenticated users can register a pet and associating
the pet with the current user. The `pet_list` view retrieves and displays
a list of all pets belonging to the logged-in user, allowing them to manage
and view their pets within the system.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PetForm
from .models import Pet


@login_required
def register_pet(request):
    """
    Handle the registration of a new pet.

    If the request method is POST, process the form data and save the pet.
    If the request method is GET, display an empty form for registering a pet.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object with the rendered template.
    """
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'pets/register_pet.html', {'form': form})


@login_required
def pet_list(request):
    """
    Display a list of pets owned by the logged-in user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object with the rendered template.
    """
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pets/pet_list.html', {'pets': pets})
