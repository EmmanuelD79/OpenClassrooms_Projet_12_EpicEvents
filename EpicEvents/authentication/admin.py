from django.contrib import admin
from authentication.models import Employee
from django.contrib.auth.models import Group


class CrmAdminArea(admin.AdminSite):
    site_header = 'EPIC EVENTS CRM'


crm_site = CrmAdminArea(name='CrmAdmin')

    
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Employee',
         {'fields': ('first_name', 'last_name', 'password', 'email', 'phone', 'mobile')}),
        ('Info', {'fields': ('date_created', 'date_updated', 'groups', 'is_staff', 'is_superuser')})
    )
    
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('full_name', 'email', 'phone', 'mobile')
    list_filter = ()
    search_fields = ['first_name', 'last_name']

    @staticmethod
    def full_name(obj):
        return f"{obj.last_name.upper()}  {obj.first_name.capitalize()}"
    
    

crm_site.register(Group)

crm_site.register(Employee, EmployeeAdmin)
