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
    list_filter = ('client_id__company_name', 'status')
    search_fields = ['amount_float', 'payment_due']

    @staticmethod
    def full_name(obj):
        return f"{obj.client_id.last_name.upper()}  {obj.client_id.first_name.capitalize()}"
    
    @staticmethod
    def company_name(obj):
        return f"{obj.client_id.company_name.upper()}"


crm_site.register(Contract, ContractAdmin)