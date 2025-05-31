from django.shortcuts import render
from .models import Event

def event_list(request):
    events = Event.objects.prefetch_related('images').order_by('-created_at')
    context = {
        'events': events,
        'current_page': 'Events',
    }

    return render(request, 'eventapp/event_list.html', context)
