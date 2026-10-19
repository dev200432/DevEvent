from urllib import request

from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Event
from registrations.models import Registration

def home(request):
    events = Event.objects.filter(
        is_active=True
    ).order_by('event_date', 'start_time')

    search = request.GET.get('search','')
    if search:
        events = events.filter(event_name__icontains=search)
    
    category = request.GET.get('category','')
    if category:
            events = events.filter(category__icontains=category)   
    event_date = request.GET.get('event_date','')
    if event_date:
        events = events.filter(event_date=event_date) 

    sort = request.GET.get('sort','upcoming')
    if sort == 'latest':
        events = events.order_by('-event_date', '-start_time')
    else:
        events = events.order_by('event_date', 'start_time')

    paginator = Paginator(events, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'events/home.html',
                  {'events': page_obj,
                   'search': search,
                   'category': category,
                   'event_date': event_date,
                   'sort': sort,

                   })
  

from django.shortcuts import render, get_object_or_404
from .models import Event
from registrations.models import Registration


def event_detail(request, id):
    event = get_object_or_404(Event, id=id)

    registered_count = Registration.objects.filter(
        event=event,
        status='registered'
    ).count()

    available_seats = max(
        0,
        event.max_participants - registered_count
    )

    if event.max_participants > 0:
        progress_percentage = min(
            100,
            int(
                (registered_count / event.max_participants) * 100
            )
        )
    else:
        progress_percentage = 0

    context = {
        'event': event,
        'registered_count': registered_count,
        'available_seats': available_seats,
        'progress_percentage': progress_percentage,
    }

    return render(
        request,
        'events/event_detail.html',
        context
    )
