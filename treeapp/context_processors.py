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
