from django.contrib import admin
from .models import Contract
from authentication.admin import crm_site
from django.contrib import messages


class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Contrat',
         {'fields': ('client_id', 'status' )}),
        ('Info', {'fields': ('sales_contact_id', 'payment_due', 'amount_float', 'date_created', 'date_updated')})
    )
    
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('client_id', 'full_name', 'company_name', 'payment_due' , 'amount_float', 'status' )
    list_filter = ('client_id__company_name', 'status', 'sales_contact_id__email')
    search_fields = ['amount_float', 'payment_due']

    @staticmethod
    def full_name(obj):
        return f"{obj.client_id.last_name.upper()}  {obj.client_id.irst_name.capitalize()}"
    
    @staticmethod
    def company_name(obj):
        return f"{obj.client_id.company_name.upper()}"
    
    def has_delete_permission(self, request, obj=None):

        if obj != None and request.POST.get('action') =='delete_selected':
            messages.add_message(request, messages.ERROR,(
                f"Merci de confirmer la suppression {obj}"
            ))

        return True

    def has_add_permission(self, request):
        
        if request.user.is_superuser:
            return False
        
        return False

    def has_change_permission(self, request, obj=None):
        
        if request.user.is_superuser:
            return True
        
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        
        return False


crm_site.register(Contract, ContractAdmin)