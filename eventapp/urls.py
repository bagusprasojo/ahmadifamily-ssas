from django.urls import path
from .views import event_list, event_detail

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:pk>/', event_detail, name='event_detail'),
]
