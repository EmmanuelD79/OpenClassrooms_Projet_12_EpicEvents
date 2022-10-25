from django.contrib import admin
from .models import Contract
from authentication.admin import crm_site


class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Contrat',
         {'fields': ('client_id', 'name', 'status' )}),
        ('Info', {'fields': ('payment_due', 'amount_float', 'date_created', 'date_updated')})
    )
    
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('name', 'full_name', 'company_name', 'payment_due' , 'amount_float', 'status' )
    list_filter = ('client_id__last_name', 'client_id__email', 'date_created', 'amount_float')
    search_fields = ['client_id__last_name', 'client_id__email', 'date_created', 'amount_float']

    def full_name(self,instance):
        return f"{instance.client_id.last_name.upper()}  {instance.client_id.first_name.capitalize()}"
    full_name.short_description = "Client"
    full_name.admin_order_field = "client_id__last_name"
    
    
    def company_name(self, instance):
        return f"{instance.client_id.company_name.upper()}"
    
    company_name.short_description = "Société"
    company_name.admin_order_field = "client_id__company_name"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(client_id__sales_contact_id=request.user)| qs.filter(event__support_contact_id=request.user)


crm_site.register(Contract, ContractAdmin)