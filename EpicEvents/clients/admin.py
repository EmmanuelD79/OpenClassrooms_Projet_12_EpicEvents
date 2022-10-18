from django.contrib import admin
from .models import Client, ClientStatus
from authentication.models import Employee
from authentication.admin import crm_site
from django.contrib.auth.models import Group, Permission
from django.contrib import messages


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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sales_contact_id":
            try:
                permission = Permission.objects.get(codename="add_client")
                groups_lst= Group.objects.filter(permissions=permission.pk).values_list('id', flat=True)
                kwargs["queryset"] = Employee.objects.filter(groups__id__in=groups_lst)
            except:
                kwargs["queryset"] = Employee.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
crm_site.register(ClientStatus)
crm_site.register(Client, ClientAdmin)

