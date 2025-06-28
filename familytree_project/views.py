from django.shortcuts import render
from eventapp.models import Event
from galleryapp.models import Gallery, GalleryImage 
from eventapp.models import  Event 
from treeapp.models import Person, AboutArticle
from datetime import datetime
from django.db.models import Q

def home(request):
    about_article = AboutArticle.objects.all().first()
    latest_event = Event.objects.order_by('-created_at').prefetch_related('images').first()
    recent_photos = GalleryImage.objects.order_by('-id')[:10]

    bulan_sekarang = datetime.now().month
    ulang_tahun_bulan_ini = Person.objects.filter(
        birth_date__month=bulan_sekarang
    ).order_by('birth_date')

    jumlah_laki_laki = Person.objects.filter(gender='M').count()
    jumlah_perempuan = Person.objects.filter(gender='F').count()
    total_keluarga = Person.objects.count()
    keluarga_terakhir = Person.objects.order_by('-created_at').first()
    print(keluarga_terakhir)

    context = {
        'current_page': 'Home',
        'about_article': about_article,
        'recent_event': latest_event,
        'jumlah_laki_laki': jumlah_laki_laki,
        'jumlah_perempuan': jumlah_perempuan,
        'total_keluarga': total_keluarga,
        'keluarga_terakhir': keluarga_terakhir,
        'recent_photos': recent_photos,
        'ulang_tahun_bulan_ini': ulang_tahun_bulan_ini,
    }

    return render(request, 'home.html', context)

def search_view(request):
    query = request.GET.get('q', '')

    if not query:
        return render(request, 'search_results.html', {'query': query, 'current_page': 'Search Results'})

    event_results = Event.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    gallery_results = Gallery.objects.filter(Q(title__icontains=query)| Q(description__icontains=query))
    person_results = Person.objects.filter(Q(name__icontains=query))

    context = {
        'query': query,
        'event_results': event_results,
        'gallery_results': gallery_results,
        'person_results': person_results,
        'current_page': 'Search Results',
    }
    return render(request, 'search_results.html', context)