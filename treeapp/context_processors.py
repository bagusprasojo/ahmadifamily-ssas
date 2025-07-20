from .models import Person, Marriage

def root_person(request):

    pasangan_root = None
    root = None;

    # print(request)
    # print(request.user)

    if request.user.is_authenticated:        
        root = Person.objects.filter(is_root=True, family = request.user.family).first()
        if root : 
            if Person.objects.all().count() > 1:
                if Marriage.objects.filter(husband=root).exists():
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