from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm

urlpatterns = [
    path('tree/input', views.input_data, name='input'),
    path('tree/<int:husband_id>/', views.family_tree, name='tree'),
    path('tree/<str:uuid>/', views.family_tree, name='tree'),
    
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='treeapp/login.html',authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('anggota/tambah/', views.tambah_anggota_view, name='tambah_anggota'),
    path('pernikahan/tambah/', views.tambah_pernikahan_view, name='tambah_pernikahan'),
    path('anak/tambah/', views.tambah_anak_view, name='tambah_anak'),


    
    
    


]
