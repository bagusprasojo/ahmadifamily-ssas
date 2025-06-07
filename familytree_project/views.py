from django.shortcuts import render
from eventapp.models import Event
from galleryapp.models import Gallery, GalleryImage 
from eventapp.models import  Event 
from treeapp.models import Person
from datetime import datetime

def home(request):
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
        'recent_event': latest_event,
        'jumlah_laki_laki': jumlah_laki_laki,
        'jumlah_perempuan': jumlah_perempuan,
        'total_keluarga': total_keluarga,
        'keluarga_terakhir': keluarga_terakhir,
        'recent_photos': recent_photos,
        'ulang_tahun_bulan_ini': ulang_tahun_bulan_ini,
    }

    return render(request, 'home.html', context)
