from django.shortcuts import render, redirect, get_object_or_404
from .models import Person, Marriage, Child
from datetime import date
from django.urls import reverse
from .forms import RegistrationForm, PersonForm, MarriageForm, ChildForm, AddChildrenForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def tambah_anak_view(request):
    family = request.user.family
    if not family:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AddChildrenForm(request.POST, family=family)
        if form.is_valid():
            marriage = form.cleaned_data['marriage']
            children = form.cleaned_data['children']
            for child in children:
                Child.objects.create(
                    person=child,
                    marriage=marriage,
                    family=family
                )
            messages.success(request, f"{children.count()} anak berhasil ditambahkan ke pernikahan.")
            return redirect('dashboard')
    else:
        form = AddChildrenForm(family=family)

    return render(request, 'treeapp/tambah_anak.html', {'form': form})


@login_required
def tambah_pernikahan_view(request):
    family = request.user.family
    if not family:
        return redirect('dashboard')

    if request.method == 'POST':
        form = MarriageForm(request.POST, family=family)
        if form.is_valid():
            marriage = form.save(commit=False)
            marriage.family = family
            marriage.save()
            return redirect('dashboard')
    else:
        form = MarriageForm(family=family)
    
    return render(request, 'treeapp/tambah_pernikahan.html', {'form': form})


@login_required
def tambah_anggota_view(request):
    if not request.user.family:
        return redirect('dashboard')

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.family = request.user.family
            person.save()
            return redirect('dashboard')
    else:
        form = PersonForm()
    
    return render(request, 'treeapp/tambah_anggota.html', {'form': form})

@login_required
def dashboard_view(request):
    family = request.user.family
    if not family:
        return redirect('register')  # jika user belum terhubung ke keluarga

    members = family.members.all()
    marriages = family.marriages.select_related('husband', 'wife').all()
    children = family.children_family.select_related('person', 'marriage__husband', 'marriage__wife').all()


    return render(request, 'treeapp/dashboard.html', {
        'family': family,
        'members': members,
        'marriages': marriages,
        'children': children,
        'user': request.user,
        'current_page': 'Dashboard Keluarga',
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # langsung login setelah register
            return redirect('dashboard')  # arahkan ke halaman keluarga atau dashboard
    else:
        form = RegistrationForm()
    return render(request, 'treeapp/register.html', {'form': form})

def input_data(request):
    person_form = PersonForm(request.POST or None, prefix='person')
    marriage_form = MarriageForm(request.POST or None, prefix='marriage')
    child_form = ChildForm(request.POST or None, prefix='child')

    if request.method == 'POST':
        if 'add_person' in request.POST and person_form.is_valid():
            person_form.save()
            return redirect('input')
        elif 'add_marriage' in request.POST and marriage_form.is_valid():
            husband = marriage_form.cleaned_data['husband']
            wife = marriage_form.cleaned_data['wife']
            date = marriage_form.cleaned_data['date_of_marriage']
            Marriage.objects.create(husband=husband, wife=wife, date_of_marriage=date)
            return redirect('input')
        elif 'add_child' in request.POST and child_form.is_valid():
            person = child_form.cleaned_data['person']
            marriage = child_form.cleaned_data['marriage']
            Child.objects.create(person=person, marriage=marriage)
            return redirect('input')

    context = {
        'person_form': person_form,
        'marriage_form': marriage_form,
        'child_form': child_form,
        'persons': Person.objects.all(),
        'current_page': 'Input Person',
    }

    return render(request, 'treeapp/input.html', context)

def build_person_node(person):
        
        # Ambil semua pernikahan sebagai suami atau istri
        if person.gender == 'M':
            marriages = Marriage.objects.filter(husband=person)
        else:
            marriages = Marriage.objects.filter(wife=person)

        marriage_data = []
        for marriage in marriages:
            spouse = marriage.wife if person.gender == 'M' else marriage.husband
            children = Child.objects.filter(marriage=marriage)

            child_nodes = []
            for child in children:
                child_nodes.append(build_person_node(child.person))  # rekursif!

            marriage_data.append({
                'spouse': {
                    'name': spouse.name,
                    'class': 'man' if spouse.gender == 'M' else 'woman',
                    "textClass": "node-text",
                    "HTMLclass": "clickable-node",
                    "extra": {
                        "person_id": spouse.id,
                        "href": reverse('person_detail', args=[spouse.id])
                    }
                },
                'children': child_nodes
            })

        return {
            'name': person.name,            
            'class': 'man' if person.gender == 'M' else 'woman',
            'marriages': marriage_data,
            "textClass": "node-text",
            "HTMLclass": "clickable-node",
            "extra": {
                "person_id": person.id,
                "href": reverse('person_detail', args=[person.id])
            }
        }


@login_required
def family_tree(request, uuid):
    persons = Person.objects.all().filter(family = request.user.family).order_by('name')
    try:
        person = Person.objects.get(uuid=uuid)
    except Person.DoesNotExist:
        return render(request, 'treeapp/tree.html', {
            'tree_data': [],
            'error': 'Data tidak ditemukan',
            'current_page': 'Family Tree',
            'persons': persons,
        })

    tree_data = [build_person_node(person)]
    # print(tree_data)

    context = {
        'tree_data': tree_data,
        'current_page': 'Family Tree',
        'husband_uuid': person.uuid,
        'persons': persons,
    }
    return render(request, 'treeapp/tree.html', context)

def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    # Hitung umur
    def hitung_umur(birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    umur = hitung_umur(person.birth_date) if person.birth_date else None


    # Cari pasangan (suami/istri)
    if person.gender == 'M':
        marriage = Marriage.objects.filter(husband=person).first()
        spouse = marriage.wife if marriage else None
    else:
        marriage = Marriage.objects.filter(wife=person).first()
        spouse = marriage.husband if marriage else None

    # Cari anak (jika dia orang tua)
    marriages_as_parent = Marriage.objects.filter(husband=person) | Marriage.objects.filter(wife=person)
    children = Person.objects.filter(child__marriage__in=marriages_as_parent)

    # Cari orang tua (jika dia anak)
    child_record = None
    try:
        child_record = Child.objects.get(person=person)
        father = child_record.marriage.husband
        mother = child_record.marriage.wife
    except Child.DoesNotExist:
        father = None
        mother = None

    # Cari saudara kandung (anak-anak dari pernikahan yang sama)
    siblings = Person.objects.none()
    if child_record:
        siblings = Person.objects.filter(child__marriage=child_record.marriage).exclude(id=person.id)

    context = {
        'person': person,
        'spouse': spouse,
        'children': children,
        'father': father,
        'mother': mother,
        'siblings': siblings,
        'umur': umur,
        'current_page': f'Profil {person.name}',
    }

    return render(request, 'treeapp/person_detail.html', context)

