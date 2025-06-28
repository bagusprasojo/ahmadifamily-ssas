from .models import Person, Marriage

def root_person(request):

    pasangan_root = None

    root = Person.objects.filter(is_root=True).first()
    if root : 
        if Person.objects.all().count() > 1:
            pasangan_root = Marriage.objects.filter(husband=root).first().wife
        

    return {
        'root_person': root,
        'pasangan_root_person': pasangan_root
    }

def app_config(request):
    from .models import AppConfig

    config = AppConfig.objects.all()
    config_dict = {item.name: item.value for item in config}

    return {
        'app_config': config_dict
    }

def image_carousel(request):
    from .models import ImageCarousel

    images = ImageCarousel.objects.all().order_by('order')

    return {
        'image_carousel': images
    }   