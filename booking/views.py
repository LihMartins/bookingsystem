"""
This module handles the core functionalities related to user interactions
with the booking system and the management of appointments. It includes views
for booking appointments, updating user and appointment information, and displaying
user and staff panels.

The functions manage tasks such as validating available dates and times, ensuring
appointments are within specified periods, and allowing users and staff to view,
edit, and manage appointments. It also includes support for displaying pets associated
with users in the user panel, with a placeholder for users without registered pets.
"""


from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from pets.models import Pet
from django.contrib import messages

def index(request):
    """
    Renders the homepage of the application.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered homepage.
    """
    return render(request, "index.html", {})

def booking(request):
    """
    Handles the booking process by displaying available days and services.

    Validates the selected day and service, stores them in the session, and
    redirects to the booking submission page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered booking page or a redirect to the booking
        submission page if a service is selected.
    """
    weekdays = validWeekday(22)
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        if service is None:
            messages.success(request, "Please Select A Service!")
            return redirect('booking')

        # Store day and service in the session
        request.session['day'] = day
        request.session['service'] = service

        return redirect('bookingSubmit')

    return render(request, 'booking.html', {
        'weekdays': weekdays,
        'validateWeekdays': validateWeekdays,
    })

def bookingSubmit(request):
    """
    Handles the final submission of a booking by validating the selected date and time.

    Ensures that the selected time is available and within the valid range before
    saving the appointment.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered booking submission page or a redirect to the
        homepage if the booking is successful.
    """
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM",
        "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    maxDate = deltatime.strftime('%Y-%m-%d')

    # Get stored data from the session
    day = request.session.get('day')
    service = request.session.get('service')

    # Only show times that haven't been selected for the selected day
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service is not None:
            if minDate <= day <= maxDate:
                if date in ['Monday', 'Saturday', 'Wednesday']:
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1:
                            Appointment.objects.get_or_create(
                                user=user,
                                service=service,
                                day=day,
                                time=time,
                            )
                            messages.success(request, "Appointment Saved!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")

    return render(request, 'bookingSubmit.html', {
        'times': hour,
    })

def userPanel(request):
    """
    Displays the user's panel with their appointments and registered pets.

    Retrieves all appointments and pets associated with the logged-in user
    and displays them on the user panel. If no pets are registered, a placeholder
    message is provided.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered user panel page.
    """
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
    pets = Pet.objects.filter(owner=user)

    # Check if no pets are registered and provide a placeholder if needed
    if not pets.exists():
        pets = [{'first_name': 'No pets registered'}]

    context = {
        'user': user,
        'appointments': appointments,
        'pets': pets,
    }
    return render(request, 'userPanel.html', context)

def userUpdate(request, id):
    """
    Handles the update of a user's appointment.

    Validates the new day and service, stores them in the session, and redirects
    to the update submission page.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the appointment to be updated.

    Returns:
        HttpResponse: The rendered appointment update page or a redirect to the
        update submission page.
    """
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    # Validate that the appointment is being edited at least 24 hours before the scheduled time
    delta24 = userdatepicked.strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    weekdays = validWeekday(22)
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        # Store day and service in the session
        request.session['day'] = day
        request.session['service'] = service

        return redirect('userUpdateSubmit', id=id)

    return render(request, 'userUpdate.html', {
        'weekdays': weekdays,
        'validateWeekdays': validateWeekdays,
        'delta24': delta24,
        'id': id,
    })

def userUpdateSubmit(request, id):
    """
    Finalizes the update of a user's appointment.

    Validates the selected time and ensures it is available before updating the appointment.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the appointment to be updated.

    Returns:
        HttpResponse: The rendered appointment update submission page or a redirect to the
        user panel.
    """
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM",
        "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    maxDate = deltatime.strftime('%Y-%m-%d')

    day = request.session.get('day')
    service = request.session.get('service')

    # Filter out times that have already been booked for the selected day, except for the current appointment time
    hour = checkEditTime(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service is not None:
            if minDate <= day <= maxDate:
                if date in ['Monday', 'Saturday', 'Wednesday']:
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            Appointment.objects.filter(pk=id).update(
                                user=user,
                                service=service,
                                day=day,
                                time=time,
                            )
                            messages.success(request, "Appointment Edited!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")
        return redirect('userPanel')

    return render(request, 'userUpdateSubmit.html', {
        'times': hour,
        'id': id,
    })

def staffPanel(request):
    """
    Displays the staff panel with a list of upcoming appointments.

    Retrieves and displays appointments scheduled within the next 21 days,
    ordered by day and time.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered staff panel page with the list of appointments.
    """
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    maxDate = deltatime.strftime('%Y-%m-%d')

    # Retrieve appointments within the next 21 days
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'staffPanel.html', {
        'items': items,
    })

def dayToWeekday(x):
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

def validWeekday(days):
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

def isWeekdayValid(x):
    """
    Filters out weekdays that are fully booked.

    Args:
        x (list): A list of weekdays as strings in the format 'YYYY-MM-DD'.

    Returns:
        list: A list of valid weekdays that are not fully booked.
    """
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def checkTime(times, day):
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

def checkEditTime(times, day, id):
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
