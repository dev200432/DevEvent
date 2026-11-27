from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking

def index(request):
    return render(request, 'index.html', {'active_page': 'index'})

def about(request):
    return render(request, 'about.html', {'active_page': 'about'})

def services(request):
    return render(request, 'services.html', {'active_page': 'services'})

def gallery(request):
    return render(request, 'gallery.html', {'active_page': 'gallery'})

def contact(request):
    return render(request, 'contact.html', {'active_page': 'contact'})

def book_event(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        event_type = request.POST.get('event_type', 'Royal Wedding').strip()
        event_date = request.POST.get('event_date')
        message = request.POST.get('message', '').strip()

        try:
            Booking.objects.create(
                name=name,
                email=email,
                phone=phone,
                event_type=event_type,
                event_date=event_date,
                message=message
            )
            messages.success(
                request,
                "Your consultation inquiry has been saved! Our team will contact you within 24 hours."
            )
        except Exception as e:
            messages.error(request, f"Error saving inquiry: {str(e)}")

        return redirect(request.META.get('HTTP_REFERER') or 'contact')

    return redirect('contact')