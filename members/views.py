"""
This module handles the authentication processes within the application,
including user login, logout, and registration. It provides views for managing
user sessions and ensuring secure access to the system. The module integrates
with Django's built-in authentication system and extends it with custom user
registration forms.

Functions:
- login_user: Authenticates and logs in a user based on provided credentials.
- logout_user: Logs out the currently logged-in user and redirects to the
homepage.
- register_user: Registers a new user, logs them in, and redirects to the
homepage.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


def login_user(request):
    """
    Authenticates and logs in a user.

    If the request method is POST, this function attempts to authenticate the
    user with the provided username and password. If successful, the user is
    logged in and redirected to the homepage. If authentication fails, an
    error message is displayed.

    Args:
        request (HttpRequest): The request object containing POST data.

    Returns:
        HttpResponse: Redirects to the homepage upon successful login, or
        re-renders the login page with an error message on failure.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('index')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, "There was an error!")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    """
    Logs out the currently authenticated user.

    This function logs out the user and displays a success message confirming
    the logout. The user is then redirected to the homepage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Redirects to the homepage after logging out.
    """
    logout(request)
    messages.success(request, "Sign out successful")
    return redirect('index')


def register_user(request):
    """
    Registers a new user and logs them in.

    If the request method is POST, this function processes the registration
    form data, creates a new user, and logs them in. A success message is
    displayed upon completion. If the method is GET, it renders a blank
    registration form.

    Args:
        request (HttpRequest): The request object containing POST data.

    Returns:
        HttpResponse: Redirects to the homepage after successful registration,
        or re-renders the registration page with validation errors.
    """
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Sign up completed!")
            return redirect('index')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {
        'form': form,
    })
