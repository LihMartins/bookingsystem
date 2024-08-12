"""
This module handles the core functionalities related to user interactions.

With the booking system and the management of appointments,
also including views for booking appointments, updating user
and appointment information, and displaying user and staff panels.

The functions manage tasks such as validating available dates and times,
ensuring appointments are within specified periods, and allowing users
and staff to view, edit, and manage appointments.
It also includes support for displaying pets associated with users
in the user panel, with a placeholder for users without registered pets.
"""


from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import Appointment
from pets.models import Pet
from django.contrib import messages


def index(request):
    """
    Render the homepage of the application.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered homepage.
    """
    return render(request, "index.html", {})


def booking(request):
    """
    Handle the booking process by displaying available days and services.

    Validates the selected day and service, stores them in the session,
    and redirects to the booking submission page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered booking page or a redirect to the booking
        submission page if a service is selected.
    """
    weekdays = valid_weekday(22)
    validate_weekdays = is_weekday_valid(weekdays)

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        if service is None:
            messages.success(request, "Please select a service!")
            return redirect('booking')

        # Store day and service in the session
        request.session['day'] = day
        request.session['service'] = service

        return redirect('booking_submit')

    return render(request, 'booking.html', {
        'weekdays': weekdays,
        'validate_weekdays': validate_weekdays,
    })


def booking_submit(request):
    """
    Handle the final submission of a booking by validating the selected
    date and time.

    Ensures that the selected time is available and within the valid range
    before saving the appointment.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered booking submission page or a redirect
        to the homepage if the booking is successful.
    """
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM",
        "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    min_date = today.strftime('%Y-%m-%d')
    delta_time = today + timedelta(days=21)
    max_date = delta_time.strftime('%Y-%m-%d')

    # Get stored data from the session
    day = request.session.get('day')
    service = request.session.get('service')

    # Only show times that haven't been selected for the selected day
    hour = check_time(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = day_to_weekday(day)

        if service is not None:
            if min_date <= day <= max_date:
                if date in ['Monday', 'Saturday', 'Wednesday']:
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1:
                            Appointment.objects.get_or_create(
                                user=user,
                                service=service,
                                day=day,
                                time=time,
                            )
                            messages.success(request, "Appointment saved!")
                            return redirect('index')
                        else:
                            messages.success(
                                request, "The selected time has been reserved before!"
                            )
                    else:
                        messages.success(request, "The selected day is full!")
                else:
                    messages.success(request, "The selected date is incorrect")
            else:
                messages.success(
                    request, "The selected date isn't in the correct time period!"
                )
        else:
            messages.success(request, "Please select a service!")

    return render(request, 'booking_submit.html', {
        'times': hour,
    })


def user_panel(request):
    """
    Display the user's panel with their appointments and registered pets.

    Retrieves all appointments and pets associated with the logged-in user
    and displays them on the user panel. If no pets are registered, a
    placeholder message is provided.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered user panel page.
    """
    user = request.user
    appointments = Appointment.objects.filter(
        user=user
    ).order_by('day', 'time')
    pets = Pet.objects.filter(owner=user)

    # Check if no pets are registered and provide a placeholder if needed
    if not pets.exists():
        pets = [{'first_name': 'No pets registered'}]

    context = {
        'user': user,
        'appointments': appointments,
        'pets': pets,
    }
    return render(request, 'user_panel.html', context)


def user_update(request, id):
    """
    Handle the update of a user's appointment.

    Validates the new day and service, stores them in the session, and
    redirects to the update submission page.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the appointment to be updated.

    Returns:
        HttpResponse: The rendered appointment update page or a redirect to
        the update submission page.
    """
    appointment = Appointment.objects.get(pk=id)
    user_date_picked = appointment.day
    today = datetime.today()
    min_date = today.strftime('%Y-%m-%d')

    # Validate that the appointment is being edited at least 24 hours before
    # the scheduled time
    delta_24 = user_date_picked.strftime(
        '%Y-%m-%d'
    ) >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    weekdays = valid_weekday(22)
    validate_weekdays = is_weekday_valid(weekdays)

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        # Check if the new date is valid and at least 24 hours ahead
        if day >= min_date:
            if delta_24:

                # Store day and service in the session
                request.session['day'] = day
                request.session['service'] = service

                return redirect('user_update_submit', id=id)
            else:
                messages.error(
                    request, "The appointment must be updated at least 24 hours in advance."
                )
        else:
            messages.error(request, "The selected date is not valid.")

    return render(request, 'user_update.html', {
        'weekdays': weekdays,
        'validate_weekdays': validate_weekdays,
        'delta_24': delta_24,
        'min_date': min_date,
        'id': id,
    })


def user_update_submit(request, id):
    """
    Finalize the update of a user's appointment.

    Validates the selected time and ensures it is available before updating
    the appointment.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the appointment to be updated.

    Returns:
        HttpResponse: The rendered appointment update submission page or a
        redirect to the user panel.
    """
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM",
        "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    min_date = today.strftime('%Y-%m-%d')
    delta_time = today + timedelta(days=21)
    max_date = delta_time.strftime('%Y-%m-%d')

    day = request.session.get('day')
    service = request.session.get('service')

    # Filter out times that have already been booked for the selected day,
    # except for the current appointment time
    hour = check_edit_time(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    user_selected_time = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = day_to_weekday(day)

        if service is not None:
            if min_date <= day <= max_date:
                if date in ['Monday', 'Saturday', 'Wednesday']:
                    if Appointment.objects.filter(day=day).count() < 11:
                        if (
                            Appointment.objects.filter(day=day, time=time).count() < 1 or
                            user_selected_time == time
                        ):
                            Appointment.objects.filter(pk=id).update(
                                user=user,
                                service=service,
                                day=day,
                                time=time,
                            )
                            messages.success(request, "Appointment edited!")
                            return redirect('index')
                        else:
                            messages.success(
                                request, "The selected time has been reserved before!"
                            )
                    else:
                        messages.success(request, "The selected day is full!")
                else:
                    messages.success(request, "The selected date is incorrect")
            else:
                messages.success(
                    request, "The selected date isn't in the correct time period!"
                )
        else:
            messages.success(request, "Please select a service!")
        return redirect('user_panel')

    return render(request, 'user_update_submit.html', {
        'times': hour,
        'id': id,
    })


def staff_panel(request):
    """
    Displays the staff panel with a list of upcoming appointments.

    Retrieves and displays appointments scheduled within the next 21 days,
    ordered by day and time.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered staff panel page with the list of
        appointments.
    """
    today = datetime.today()
    min_date = today.strftime('%Y-%m-%d')
    delta_time = today + timedelta(days=21)
    max_date = delta_time.strftime('%Y-%m-%d')

    # Retrieve appointments within the next 21 days
    items = Appointment.objects.filter(day__range=[min_date, max_date]).order_by(
        'day', 'time'
    )

    return render(request, 'staff_panel.html', {
        'items': items,
    })


def day_to_weekday(x):
    """
    Converts a date string to the corresponding weekday name.

    Args:
        x (str): The date string in the format 'YYYY-MM-DD'.

    Returns:
        str: The name of the weekday for the given date.
    """
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y


def valid_weekday(days):
    """
    Generates a list of valid weekdays (Monday, Wednesday, and Saturday)
    within the next specified number of days.

    Args:
        days (int): The number of days from today to consider.

    Returns:
        list: A list of valid weekdays as strings in the format 'YYYY-MM-DD'.
    """
    today = datetime.now()
    weekdays = []
    for i in range(days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y in ['Monday', 'Saturday', 'Wednesday']:
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays


def is_weekday_valid(x):
    """
    Filters out weekdays that are fully booked.

    Args:
        x (list): A list of weekdays as strings in the format 'YYYY-MM-DD'.

    Returns:
        list: A list of valid weekdays that are not fully booked.
    """
    validate_weekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validate_weekdays.append(j)
    return validate_weekdays


def check_time(times, day):
    """
    Filters out times that have already been selected for a specific day.

    Args:
        times (list): A list of time slots.
        day (str): The date for which to check the time slots.

    Returns:
        list: A list of available time slots for the given day.
    """
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x


def check_edit_time(times, day, id):
    """
    Filters out time slots that have already been selected, excluding the
    current appointment's time.

    Args:
        times (list): A list of time slots.
        day (str): The date for which to check the time slots.
        id (int): The ID of the appointment being edited.

    Returns:
        list: A list of available time slots for the given day, including the
        current appointment's time slot.
    """
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x
