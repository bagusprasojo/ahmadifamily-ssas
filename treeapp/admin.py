from django.contrib import admin
from .models import Person, Marriage, Child, VisitorLog
from django.utils.timezone import localtime

class MarriageInline(admin.ModelAdmin):
    list_display = ('husband', 'wife', 'date_of_marriage')
    search_fields = ('husband__name', 'wife__name')

class ChildInline(admin.ModelAdmin):
    list_display = ('person', 'marriage')
    search_fields = ('person__name', 'marriage__husband__name', 'marriage__wife__name')
    
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name','gender','birth_date', 'created_at', 'updated_at', 'is_root')
    search_fields = ('name',)

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    # local_time = localtime(log.timestamp)
    list_display = ('ip_address', 'path', 'timestamp')
    search_fields = ('ip_address', 'path', 'user_agent')
    list_filter = ('timestamp',)

admin.site.register(Person, PersonAdmin)
admin.site.register(Marriage, MarriageInline)
admin.site.register(Child, ChildInline)

