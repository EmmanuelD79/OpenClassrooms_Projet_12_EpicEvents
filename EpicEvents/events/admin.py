from django.contrib import admin
from .models import Event, EventStatus
from authentication.admin import crm_site


class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Event',
         {'fields': ('contract_id', 'event_status', 'notes')}),
        ('Info', {'fields': ('support_contact_id', 'event_date', 'attendees', 'date_created', 'date_updated')})
    )
    
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('contract_id', 'event_status')
    list_filter = ('event_status', 'contract_id__client_id__last_name', 'contract_id__client_id__email' )
    search_fields = ['event_date', 'contract_id__client_id__last_name', 'contract_id__client_id__email' ]

    @staticmethod
    def full_name(obj):
        return f"{obj.contract_id.client_id.last_name.upper()}  {obj.contract_id.client_id.first_name.capitalize()}"
    
    @staticmethod
    def company_name(obj):
        return f"{obj.contract_id.client_id.company_name.upper()}"
    
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "support_contact_id":
    #         try:
    #             permission = Permission.objects.get(codename="add_event")
    #             groups_lst= Group.objects.filter(permissions=permission.pk).values_list('id', flat=True)
    #             kwargs["queryset"] = Employee.objects.filter(groups__id__in=groups_lst)
    #         except:
    #             kwargs["queryset"] = Employee.objects.all()  

    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj = None, ** kwargs):
        form = super().get_form(request, obj = None, ** kwargs)
        try:
            form.base_fields["support_contact_id"].disabled = True
        except KeyError:
            pass
        if request.user.is_superuser:
            form.base_fields["support_contact_id"].disabled = False

        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(contract_id__client_id__sales_contact_id=request.user) | qs.filter(support_contact_id=request.user)
    
    
crm_site.register(EventStatus)
crm_site.register(Event, EventAdmin)

