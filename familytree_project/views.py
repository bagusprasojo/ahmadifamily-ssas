from django.shortcuts import render
from eventapp.models import Event
from galleryapp.models import Gallery, GalleryImage 
from eventapp.models import  Event 
from treeapp.models import Person

def home(request):
    latest_event = Event.objects.order_by('-created_at').prefetch_related('images').first()
    latest_gallery = Gallery.objects.order_by('-created_at').prefetch_related('images').first()
    recent_photos = GalleryImage.objects.order_by('-id')[:10]

    jumlah_laki_laki = Person.objects.filter(gender='M').count()
    jumlah_perempuan = Person.objects.filter(gender='F').count()
    total_keluarga = Person.objects.count()
    keluarga_terakhir = Person.objects.order_by('-created_at').first()
    print(keluarga_terakhir)

    context = {
        'current_page': 'Home',
        'latest_event': latest_event,
        'latest_gallery': latest_gallery,
        'jumlah_laki_laki': jumlah_laki_laki,
        'jumlah_perempuan': jumlah_perempuan,
        'total_keluarga': total_keluarga,
        'keluarga_terakhir': keluarga_terakhir,
        'recent_photos': recent_photos,
    }

    return render(request, 'home.html', context)
