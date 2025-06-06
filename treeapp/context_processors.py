from .models import Person

def root_person(request):
    root = Person.objects.filter(is_root=True).first()
    return {
        'root_person': root
    }
