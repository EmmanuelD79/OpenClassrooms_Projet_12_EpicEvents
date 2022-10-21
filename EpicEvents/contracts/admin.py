from django.contrib import admin
from .models import Contract
from authentication.admin import crm_site
from django.contrib import messages


class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Contrat',
         {'fields': ('client_id', 'name', 'status' )}),
        ('Info', {'fields': ('payment_due', 'amount_float', 'date_created', 'date_updated')})
    )
    
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('client_id', 'full_name', 'company_name', 'payment_due' , 'amount_float', 'status' )
    list_filter = ('client_id__last_name', 'client_id__email', 'date_created', 'amount_float')
    search_fields = ['client_id__last_name', 'client_id__email', 'date_created', 'amount_float']

    @staticmethod
    def full_name(obj):
        return f"{obj.client_id.last_name.upper()}  {obj.client_id.first_name.capitalize()}"
    
    @staticmethod
    def company_name(obj):
        return f"{obj.client_id.company_name.upper()}"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(client_id__sales_contact_id=request.user)| qs.filter(event__support_contact_id=request.user)


crm_site.register(Contract, ContractAdmin)