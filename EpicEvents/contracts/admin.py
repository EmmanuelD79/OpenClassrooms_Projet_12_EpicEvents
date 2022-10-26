from django.contrib import admin
from contracts.models import Contract
from authentication.admin import crm_site
from clients.models import Client


class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Contrat',
         {'fields': ('client_id', 'name', 'status')}),
        ('Info', {'fields': ('payment_due', 'amount_float', 'date_created', 'date_updated')})
    )

    readonly_fields = ('date_created', 'date_updated')
    list_display = (
        'name',
        'full_name',
        'company_name',
        'payment_due',
        'amount_float',
        'status')
    list_filter = ('client_id__last_name', 'client_id__email', 'date_created', 'amount_float')
    search_fields = ['client_id__last_name', 'client_id__email', 'date_created', 'amount_float']

    def full_name(self, instance):
        return f"{instance.client_id.last_name.upper()}  {instance.client_id.first_name.capitalize()}"
    full_name.short_description = "Client"
    full_name.admin_order_field = "client_id__last_name"

    def company_name(self, instance):
        return f"{instance.client_id.company_name.upper()}"

    company_name.short_description = "Société"
    company_name.admin_order_field = "client_id__company_name"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:
            add_view = request.path.split("/")[-2]
            if db_field.name == "client_id" and add_view == 'add':
                kwargs["queryset"] = Client.objects.filter(
                    sales_contact_id=request.user) | Client.objects.filter(
                        contract__event__support_contact_id=request.user
                        )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=None, ** kwargs)

        if kwargs['change'] and len(form.base_fields) > 0:
            form.base_fields["client_id"].disabled = True
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(client_id__sales_contact_id=request.user) | qs.filter(event__support_contact_id=request.user)


crm_site.register(Contract, ContractAdmin)
