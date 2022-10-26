from django.contrib import admin
from .models import Client, ClientStatus
from authentication.models import Employee
from authentication.admin import crm_site
from django.contrib.auth.models import Group, Permission
from contracts.models import Contract
from django.core.exceptions import ObjectDoesNotExist


class ContractItemAdmin(admin.TabularInline):
    model = Contract


class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Client',
         {'fields': ('first_name', 'last_name', 'email', 'phone', 'mobile')}),
        ('Info', {'fields': ('company_name', 'sales_contact_id', 'status', 'date_created', 'date_updated')})
    )

    readonly_fields = ('date_created', 'date_updated')
    list_display = ('full_name', 'email', 'phone', 'mobile', 'company_name', 'status')
    list_filter = ('last_name', 'email')
    search_fields = ['last_name', 'email']

    inlines = [ContractItemAdmin]

    def full_name(self, instance):
        return f"{instance.last_name.upper()}  {instance.first_name.capitalize()}"

    full_name.short_description = "Client"
    full_name.admin_order_field = "last_name"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sales_contact_id":
            try:
                permission = Permission.objects.get(codename="add_client")
                groups_lst = Group.objects.filter(permissions=permission.pk).values_list('id', flat=True)
                kwargs["queryset"] = Employee.objects.filter(groups__id__in=groups_lst)
            except ObjectDoesNotExist:
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sales_contact_id=request.user) | qs.filter(contract__event__support_contact_id=request.user)


crm_site.register(ClientStatus)
crm_site.register(Client, ClientAdmin)
