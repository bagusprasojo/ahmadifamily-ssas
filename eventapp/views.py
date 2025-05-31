from django.shortcuts import render, get_object_or_404
from .models import Event

def event_list(request):
    events = Event.objects.prefetch_related('images').order_by('-created_at')
    context = {
        'events': events,
        'current_page': 'Events',
    }

    return render(request, 'eventapp/event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'eventapp/event_detail.html', {'event': event})
