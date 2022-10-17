from django.contrib import admin
from .models import Client, ClientStatus
from authentication.admin import crm_site
from django.contrib import messages


class CLientStatusAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):

        if obj != None and request.POST.get('action') =='delete_selected':
            messages.add_message(request, messages.ERROR,(
                f"Merci de confirmer la suppression {obj}"
            ))

        if request.user.is_staff:
            return True
        return True

    def has_add_permission(self, request):
        
        if request.user.is_staff:
            return True
        return True

    def has_change_permission(self, request, obj=None):
        
        if request.user.is_staff:
            return True
        return True

    def has_view_permission(self, request, obj=None):
        
        if request.user.is_staff:
            return True
        return True

class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Client',
         {'fields': ('first_name', 'last_name', 'email', 'phone', 'mobile')}),
        ('Info', {'fields': ('company_name', 'sales_contact_id', 'status', 'date_created', 'date_updated')})
    )
    
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('full_name', 'email', 'phone', 'mobile', 'company_name', 'status' )
    list_filter = ('company_name', 'status', 'sales_contact_id__email')
    search_fields = ['first_name', 'last_name', 'company_name', 'sales_contact_id__email' ]

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
        
        if request.user.is_staff:
            return True
        return True

    def has_change_permission(self, request, obj=None):
        
        if request.user.is_staff:
            return True
        return True

    def has_view_permission(self, request, obj=None):
        
        if request.user.is_staff:
            return True
        return True
   
    
crm_site.register(ClientStatus, CLientStatusAdmin)
crm_site.register(Client, ClientAdmin)

