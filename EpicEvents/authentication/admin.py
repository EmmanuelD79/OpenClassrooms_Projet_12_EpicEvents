from django.contrib import admin
from authentication.models import Employee, Group
from django.contrib import messages


class CrmAdminArea(admin.AdminSite):
    site_header = 'EPIC EVENTS CRM'


crm_site = CrmAdminArea(name='CrmAdmin')

class GroupAdminPermissions(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):

        if obj != None and request.POST.get('action') =='delete_selected':
            messages.add_message(request, messages.ERROR,(
                f"Merci de confirmer la suppression {obj}"
            ))

        return True

    def has_add_permission(self, request):
        
        return True

    def has_change_permission(self, request, obj=None):
        
        if request.user.is_superuser:
            return True
        
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        
        return False

    
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Employee',
         {'fields': ('first_name', 'last_name', 'email', 'phone', 'mobile')}),
        ('Info', {'fields': ('date_created', 'date_updated', 'group_name', 'is_staff', 'is_superuser')})
    )
    
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('full_name', 'email', 'phone', 'mobile', 'group_name')
    list_filter = ('group_name__name',)
    search_fields = ['first_name', 'last_name', 'group_name__name']

    @staticmethod
    def full_name(obj):
        return f"{obj.last_name.upper()}  {obj.first_name.capitalize()}"
    
    def has_delete_permission(self, request, obj=None):

        if obj != None and request.POST.get('action') =='delete_selected':
            messages.add_message(request, messages.ERROR,(
                f"Merci de confirmer la suppression {obj}"
            ))

        return True

    def has_add_permission(self, request):
        
        if request.user.is_superuser:
            return True
        
        return False

    def has_change_permission(self, request, obj=None):
        
        if request.user.is_superuser:
            return True
        
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        return False


crm_site.register(Group, GroupAdminPermissions)

crm_site.register(Employee, EmployeeAdmin)
