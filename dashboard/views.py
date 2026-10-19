from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

from events.models import Event
from registrations.models import Registration

from django.utils import timezone


@staff_member_required(login_url='/admin/login/')
def dashboard_home(request):

    # Current Date and Time
    current_time = timezone.localtime()
    current_date = current_time.date()
    current_clock = current_time.time()

    # Dashboard Statistics
    total_events = Event.objects.count()
    total_users = User.objects.count()
    total_registrations = Registration.objects.count()

    active_registrations = Registration.objects.filter(
        status='registered'
    ).count()

    cancelled_registrations = Registration.objects.filter(
        status='cancelled'
    ).count()

    # Event Search
    search_query = request.GET.get('search', '').strip()

    # Category Filter
    selected_category = request.GET.get('category', '').strip()

    # Base Query
    events = Event.objects.all()

    # Search by Event Name
    if search_query:
        events = events.filter(
            event_name__icontains=search_query
        )

    # Filter by Category
    if selected_category:
        events = events.filter(
            category=selected_category
        )

    # Sort Events by Date and Time
    events = events.order_by('event_date', 'start_time')

    # Show Filtered Events
    upcoming_events = list(events[:20])

    # Event Status
    for event in upcoming_events:

        if not event.is_active:
            event.event_status = 'Inactive'

        elif event.event_date < current_date:
            event.event_status = 'Completed'

        elif event.event_date > current_date:
            event.event_status = 'Upcoming'

        elif current_clock < event.start_time:
            event.event_status = 'Upcoming'

        elif current_clock <= event.end_time:
            event.event_status = 'Ongoing'

        else:
            event.event_status = 'Completed'

    # Recent Registrations
    recent_registrations = Registration.objects.select_related(
        'user', 'event'
    ).order_by('-id')[:5]

    # Category Choices
    categories = Event.CATEGORY_CHOICES

    # Context
    context = {
        'total_events': total_events,
        'total_users': total_users,
        'total_registrations': total_registrations,
        'active_registrations': active_registrations,
        'cancelled_registrations': cancelled_registrations,
        'upcoming_events': upcoming_events,
        'recent_registrations': recent_registrations,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )