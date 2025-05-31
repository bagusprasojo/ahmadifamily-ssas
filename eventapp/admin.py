from django.contrib import admin
from .models import Event, EventImage
from ckeditor.widgets import CKEditorWidget
from django import forms

class EventAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Event
        fields = '__all__'

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    inlines = [EventImageInline]
    list_display = ('title', 'created_at')
