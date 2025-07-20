from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Family, Person, Marriage, Child
from django.contrib.auth.forms import AuthenticationForm

class AddSpouseForm(forms.Form):
    person = forms.ModelChoiceField(
        queryset=Person.objects.none(),  # akan diisi di __init__
        label="Pilih Anggota",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    spouse_name = forms.CharField(
        label="Nama Pasangan",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    spouse_gender = forms.ChoiceField(
        choices=Person.GENDER_CHOICES,
        label="Jenis Kelamin Pasangan",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    date_of_marriage = forms.DateField(
        required=False,
        label="Tanggal Pernikahan",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        family = kwargs.pop("family", None)
        super().__init__(*args, **kwargs)
        if family:
            self.fields['person'].queryset = Person.objects.filter(family=family)

class AddChildrenFormTree(forms.Form):
    marriage = forms.ModelChoiceField(
        queryset=Marriage.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Pilih Pernikahan"
    )
    
    child_name = forms.CharField(
        label="Nama Anak",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    child_gender = forms.ChoiceField(
        choices=Person.GENDER_CHOICES,
        label="Jenis Kelamin Anak",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, **kwargs):
        family = kwargs.pop('family', None)
        super().__init__(*args, **kwargs)
        if family:
            self.fields['marriage'].queryset = family.marriages.all()
            


class AddChildrenForm(forms.Form):
    marriage = forms.ModelChoiceField(
        queryset=Marriage.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Pilih Pernikahan"
    )
    children = forms.ModelMultipleChoiceField(
        queryset=Person.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '10'}),
        label="Pilih Anak-anak"
    )

    def __init__(self, *args, **kwargs):
        family = kwargs.pop('family', None)
        super().__init__(*args, **kwargs)
        if family:
            self.fields['marriage'].queryset = family.marriages.all()
            # filter hanya anak yang belum jadi child dari marriage
            anak_yang_belum_dipasangkan = Person.objects.filter(family=family).exclude(
                id__in=Child.objects.filter(family=family).values_list('person_id', flat=True)
            )
            self.fields['children'].queryset = anak_yang_belum_dipasangkan


class MarriageForm(forms.ModelForm):
    class Meta:
        model = Marriage
        fields = ['husband', 'wife', 'date_of_marriage']
        widgets = {
            'husband': forms.Select(attrs={'class': 'form-select'}),
            'wife': forms.Select(attrs={'class': 'form-select'}),
            'date_of_marriage': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        family = kwargs.pop('family', None)
        super().__init__(*args, **kwargs)
        if family:
            self.fields['husband'].queryset = family.members.filter(gender='M')
            self.fields['wife'].queryset = family.members.filter(gender='F')


class ChildForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Person.objects.all())
    marriage = forms.ModelChoiceField(queryset=Marriage.objects.all())

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'gender', 'birth_date', 'is_root']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_root': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Masukkan username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Masukkan password'
    }))
    


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    family_name = forms.CharField(
        label="Family Name",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Keluarga'})
    )

    # ✅ Ini dia: override langsung kedua password field
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Ulangi Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ulangi Password'}),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "family_name")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        family_name = self.cleaned_data['family_name']
        family = Family.objects.create(name=family_name, slug=family_name.lower().replace(" ", "-"))
        user.family = family
        user.role = 'admin'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user