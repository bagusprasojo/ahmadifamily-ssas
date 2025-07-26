from django.shortcuts import render, redirect, get_object_or_404
from .models import Person, Marriage, Child
from datetime import date
from django.urls import reverse
from .forms import RegistrationForm, PersonForm, MarriageForm, ChildForm, AddChildrenForm, AddSpouseForm, AddChildrenFormTree
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import RestrictedError
from django.db import models
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt


@login_required
def tambah_pasangan_view(request):
    family = request.user.family
    print(f"Family: {family}")
    if not family:
        return redirect('dashboard')

    if request.method == 'POST':      
        print("POST request received")  
        form = AddSpouseForm(request.POST, family=family)
        # print(form.cleaned_data)
        print(form.errors)
        if form.is_valid():
            # Ambil data form
            print(form.cleaned_data)
            target_person = form.cleaned_data['person']
            spouse_name = form.cleaned_data['spouse_name']
            spouse_gender = form.cleaned_data['spouse_gender']
            date_of_marriage = form.cleaned_data['date_of_marriage']
            
                

            # Buat pasangan baru
            spouse = Person.objects.create(
                name=spouse_name,
                gender=spouse_gender,
                family=family
            )

            # Tentukan mana husband dan wife
            if target_person.gender == 'M':
                husband, wife = target_person, spouse
            else:
                husband, wife = spouse, target_person

            # Buat record pernikahan
            Marriage.objects.create(
                husband=husband,
                wife=wife,
                date_of_marriage=date_of_marriage,
                family=family
            )

            # messages.success(request, f"Pasangan '{spouse_name}' berhasil ditambahkan.")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = AddSpouseForm(family=family)

    return render(request, 'treeapp/tambah_pasangan.html', {'form': form})

@login_required
def tambah_anak_tree(request):
    family = request.user.family
    print(f"Family: {family}")
    if not family:
        return redirect('dashboard')

    if request.method == 'POST':      
        print("POST request received")  
        form = AddChildrenFormTree(request.POST, family=family)
        # print(form.cleaned_data)
        print(form.errors)
        if form.is_valid():
            # Ambil data form
            print(form.cleaned_data)
            marriage = form.cleaned_data['marriage']
            child_name = form.cleaned_data['child_name']
            child_gender = form.cleaned_data['child_gender']
            
            # Buat pasangan baru
            child = Person.objects.create(
                name=child_name,
                gender=child_gender,
                family=family
            )

            Child.objects.create(
                    person=child,
                    marriage=marriage,
                    family=family
                )

            # messages.success(request, f"Pasangan '{spouse_name}' berhasil ditambahkan.")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = AddSpouseForm(family=family)

    return render(request, 'treeapp/tambah_pasangan.html', {'form': form})


def build_tree_node(person, family):
    node = {
        "text": {
            "name": person.name
        },
        "collapsed": True,  # Node akan collapsed secara default
        "HTMLclass": "clickable-node",
        "extra": {
            "person_id": person.id,
            "href": reverse('person_detail', args=[person.uuid]),
            "label": person.name,
        }
    }

    # Cari pasangan orang ini (jika ada)
    marriages = Marriage.objects.filter(family=family).filter(
        models.Q(husband=person) | models.Q(wife=person)
    )

    children_nodes = []

    for marriage in marriages:
        # Ambil semua anak dari pernikahan ini
        anak_list = Child.objects.filter(marriage=marriage).select_related('person')

        for anak in anak_list:
            # Rekursif ke anaknya
            child_node = build_tree_node(anak.person, family)
            children_nodes.append(child_node)

        # Tambahkan pasangan jika ingin ditampilkan di satu node (opsional)
        pasangan = marriage.wife if marriage.husband == person else marriage.husband
        node["text"]["name"] += f" + {pasangan.name}"

    if children_nodes:
        node["children"] = children_nodes

    return node

@login_required
def tree_view(request):
    return render(request, 'treeapp/tree_view.html')

@login_required
def tree_json_view(request):
    family = request.user.family
    # Tentukan siapa rootnya (misalnya orang pertama yang terdaftar di family ini)
    root_person = Person.objects.filter(family=family).first()

    if not root_person:
        return JsonResponse({"error": "Tidak ada anggota keluarga."})

    tree_structure = {
        "chart": {
            "container": "#tree-simple",
            "collapsable": False,  # Aktifkan collapse/expand
            "connectors": {
                "type": "bCurve",
                "style": {
                    "stroke": "#0d1fe6",
                    "stroke-width": 2
                }
            },
            "node": {
                "HTMLclass": "nodeExample1"
            },
            "animation": {
                "nodeAnimation": "easeOutBounce",
                "nodeSpeed": 700,
                "connectorsAnimation": "bounce",
                "connectorsSpeed": 700
            }
        },
        "nodeStructure": build_tree_node(root_person, family)
    }

    return JsonResponse(tree_structure)

@login_required
def hapus_anak_view(request, uuid):
    family = request.user.family
    child = get_object_or_404(Child, uuid=uuid, family=family)

    if request.method == 'POST':
        try:
            child.delete()
            messages.success(request, f'Anak "{child.person.name}" berhasil dihapus dari pernikahan.')
        except RestrictedError:
            messages.error(request, "Tidak dapat menghapus karena data ini masih terkait dengan entitas lain.")
        return redirect('dashboard')

    return render(request, 'treeapp/konfirmasi_hapus.html', {
        'caption': 'Hapus Anak',
        'pesan': f'Apakah Anda yakin ingin menghapus anak "{child.person.name}" dari pernikahan {child.marriage.husband.name} dan {child.marriage.wife.name}?', 
    })


@login_required
def hapus_pernikahan_view(request, uuid):
    family = request.user.family
    marriage = get_object_or_404(Marriage, uuid=uuid, family=family)

    if request.method == 'POST':
        try:
            marriage.delete()
            messages.success(request, "Pernikahan berhasil dihapus.")
        except RestrictedError:
            messages.error(request, "Tidak dapat menghapus pernikahan karena terkait data lain.")
        return redirect('dashboard')

    return render(request, 'treeapp/konfirmasi_hapus.html', {
        'caption': 'Hapus Pernikahan',
        'pesan': f'Apakah Anda yakin ingin menghapus pernikahan antara {marriage.husband.name} dan {marriage.wife.name}?',
    })

@login_required
def hapus_anggota_view(request, uuid):
    person = get_object_or_404(Person, uuid=uuid, family=request.user.family)

    if request.method == 'POST':
        try:
            person.delete()
            messages.success(request, f'Anggota "{person.name}" berhasil dihapus.')
            return redirect('dashboard')
        except RestrictedError as e:
            messages.error(request, f'Tidak bisa menghapus anggota "{person.name}". Karena ada data yang terkait')
            return redirect('dashboard')

    return render(request, 'treeapp/konfirmasi_hapus.html', {
        'caption': 'Hapus Anggota',
        'pesan': f'Apakah Anda yakin ingin menghapus anggota "{person.name}" dari keluarga Anda?',
    })

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
def tambah_or_edit_pernikahan_view(request, uuid=None):
    family = request.user.family
    if not family:
        return redirect('dashboard')

    # Cek apakah sedang edit
    if uuid:
        marriage = get_object_or_404(Marriage, uuid=uuid, family=family)
    else:
        marriage = None

    if request.method == 'POST':
        form = MarriageForm(request.POST, family=family, instance=marriage)
        if form.is_valid():
            marriage_obj = form.save(commit=False)
            marriage_obj.family = family
            marriage_obj.save()
            return redirect('dashboard')
    else:
        form = MarriageForm(family=family, instance=marriage)

    return render(request, 'treeapp/tambah_pernikahan.html', {
        'form': form,
        'edit_mode': bool(marriage),
        'marriage': marriage,
    })


@login_required
def tambah_or_edit_anggota_view(request, url_asal, uuid=None):
    if not request.user.family:
        return redirect('dashboard')

    if uuid:
        person = get_object_or_404(Person, uuid=uuid, family=request.user.family)
    else:
        person = None

    if url_asal == False:
        url_asal = 'dashboard'
    elif url_asal != 'dashboard':
        url_asal = reverse('tree', args=[url_asal])

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            new_person = form.save(commit=False)
            new_person.family = request.user.family
            new_person.save()
            messages.success(request, f'Anggota "{new_person.name}" berhasil {"ditambahkan" if not person else "diperbarui"}.')
            
            return redirect(url_asal)
    else:
        form = PersonForm(instance=person)

    return render(request, 'treeapp/tambah_anggota.html', {
        'form': form,
        'edit_mode': bool(person),
        'person': person,
        'url_asal':url_asal
    })


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

@csrf_exempt
def family_tree_json(request, person_uuid):
    """
    Endpoint publik untuk menghasilkan JSON pohon keluarga.
    Bisa diakses siapa saja (tanpa login).
    """
    try:
        person = get_object_or_404(Person, uuid=person_uuid)
        tree_data = build_person_node(person)
        return JsonResponse(tree_data, safe=False)
    except Http404:
        return JsonResponse({'error': 'Person not found'}, status=404)
    
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
                    'class': ('man' if spouse.gender == 'M' else 'woman') + ' pasangan',
                    "textClass": "node-text",
                    "HTMLclass": "clickable-node",
                    "extra": {
                        "person_id": spouse.id,
                        "is_inti": 0,
                        "href": reverse('tree', args=[spouse.uuid]),
                        "href_edit": reverse('edit_anggota', args=['abcdefg',spouse.uuid]),
                        "marriage_id":marriage.id
                    }
                },
                'children': child_nodes
            })


        return {
            'name': person.name,            
            'class': ('man' if person.gender == 'M' else 'woman') + ' inti',
            'marriages': marriage_data,
            "textClass": "node-text",
            "HTMLclass": "clickable-node",
            "extra": {
                "person_id": person.id,
                "pk_id": person.id,
                "is_inti": 1,                
                "href": reverse('tree', args=[person.uuid]),
                "href_edit": reverse('edit_anggota', args=['abcdefg',person.uuid])
                
            }
        }


@login_required
def family_tree(request, uuid=None):
    persons = Person.objects.all().filter(family = request.user.family).order_by('name')
    form = AddSpouseForm(family=request.user.family)
    form_anak_tree = AddChildrenFormTree(family=request.user.family)
        
    if uuid:
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
            'form': form,
            'form_anak_tree':form_anak_tree
        }
        # return render(request, 'treeapp/tree.html', context)
    else:
        context = {
            'current_page': 'Family Tree',
            'persons': persons,
            'form': form,
            'form_anak_tree':form_anak_tree
        }
    
    return render(request, 'treeapp/tree.html', context)

def person_detail(request, uuid):
    person = get_object_or_404(Person, uuid=uuid)

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

