"""
URL configuration for familytree_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: views.home_dashboard(request) if request.user.is_authenticated else views.home_public(request), name='home'),
    path('home/', views.home_dashboard, name='home_dashboard'),
    path('landing/', views.home_public, name='home_public'),
    path('', include('treeapp.urls')),
    path('events/', include('eventapp.urls')),
    path('gallery/', include('galleryapp.urls')),
    path('search/', views.search_view, name='search'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
