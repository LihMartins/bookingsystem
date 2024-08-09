from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PetForm
from .models import Pet

@login_required
def register_pet(request):
    """
    Handles the registration of a new pet.

    If the request method is POST, it processes the form data and saves the pet.
    If the request method is GET, it displays an empty form for registering a pet.

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
    Displays a list of pets owned by the logged-in user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object with the rendered template.
    """
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pets/pet_list.html', {'pets': pets})
