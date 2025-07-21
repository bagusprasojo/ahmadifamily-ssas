from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm

urlpatterns = [
    path('tree/input', views.input_data, name='input'),
    path('tree/<int:husband_id>/', views.family_tree, name='tree'),
    path('tree/', views.family_tree, name='tree'),
    path('tree/<str:uuid>/', views.family_tree, name='tree'),
    path('pohon/', views.tree_view, name='tree_view'),
    path('pohon/json/', views.tree_json_view, name='tree_json_view'),

    
    path('person/<str:uuid>/', views.person_detail, name='person_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='treeapp/login.html',authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    path('anggota/tambah/<str:url_asal>', views.tambah_or_edit_anggota_view, name='tambah_anggota'),
    path('anggota/<str:url_asal>/<str:uuid>/edit/', views.tambah_or_edit_anggota_view, name='edit_anggota'),
    path('anggota/<str:uuid>/hapus/', views.hapus_anggota_view, name='hapus_anggota'),

    path('pernikahan/tambah/', views.tambah_or_edit_pernikahan_view, name='tambah_pernikahan'),
    path('pernikahan/<str:uuid>/edit/', views.tambah_or_edit_pernikahan_view, name='edit_pernikahan'),
    path('pernikahan/<str:uuid>/hapus/', views.hapus_pernikahan_view, name='hapus_pernikahan'),

    path('anak/tambah/', views.tambah_anak_view, name='tambah_anak'),
    path('anak/tambah_tree/', views.tambah_anak_tree, name='tambah_anak_tree'),
    path('anak/<str:uuid>/hapus/', views.hapus_anak_view, name='hapus_anak'),
    path('tambah_pasangan/', views.tambah_pasangan_view, name='tambah_pasangan'),
    





    
    
    


]
