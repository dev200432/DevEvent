
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from events.models import Event
from .models import Registration

@login_required(login_url='login')
def register_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    # Check whether the event is active
    if not event.is_active:
        messages.error(
            request,
            'This event is currently inactive.'
        )
        return redirect('event_detail', id=event.id)

    # Check whether the event has already ended
    now = timezone.localtime()
    current_date = now.date()
    current_time = now.time()

    if event.event_date < current_date:
        messages.error(
            request,
            'Registration is closed because this event has passed.'
        )
        return redirect('event_detail', id=event.id)

    if (
        event.event_date == current_date
        and current_time >= event.end_time
    ):
        messages.error(
            request,
            'Registration is closed because this event has ended.'
        )
        return redirect('event_detail', id=event.id)

    # Find existing registration
    registration = Registration.objects.filter(
        user=request.user,
        event=event
    ).first()

    # Prevent duplicate registration
    if registration and registration.status == 'registered':
        messages.warning(
            request,
            'You are already registered for this event.'
        )
        return redirect('event_detail', id=event.id)

    # Count currently registered participants
    registered_count = Registration.objects.filter(
        event=event,
        status='registered'
    ).count()

    # Check available seats
    if registered_count >= event.max_participants:
        messages.error(
            request,
            'Sorry! All seats for this event are filled.'
        )
        return redirect('event_detail', id=event.id)

    # Reactivate a cancelled registration
    if registration:
        registration.status = 'registered'
        registration.save(update_fields=['status'])

        messages.success(
            request,
            'You have successfully registered for this event again!'
        )

    # Create a new registration
    else:
        Registration.objects.create(
            user=request.user,
            event=event
        )

        messages.success(
            request,
            'You have successfully registered for this event!'
        )

    return redirect('event_detail', id=event.id)


@login_required(login_url='login')
def my_registrations(request):

    registrations = Registration.objects.filter(
        user=request.user
    ).select_related(
        'event'
    ).order_by('-registration_date')

    return render(
        request,
        'registrations/my_registrations.html',
        {
            'registrations': registrations
        }
    )



@login_required(login_url='login')
def cancel_registration(request, registration_id):

    if request.method != 'POST':
        messages.error(
            request,
            'Please use the Cancel Registration button.'
        )
        return redirect('my_registrations')

    registration = get_object_or_404(
        Registration,
        id=registration_id,
        user=request.user
    )

    if registration.status == 'registered':
        registration.status = 'cancelled'
        registration.save(update_fields=['status'])

        messages.success(
            request,
            'Your registration has been cancelled successfully.'
        )
    else:
        messages.info(
            request,
            'This registration has already been cancelled.'
        )

    return redirect('my_registrations')
