from django.contrib import admin
from .models import Event, EventStatus
from authentication.admin import crm_site
from authentication.models import Employee
from contracts.models import Contract
from events.models import Event

class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Event',
         {'fields': ('contract_id', 'event_status', 'notes')}),
        ('Info', {'fields': ('support_contact_id', 'event_date', 'attendees', 'date_created', 'date_updated')})
    )
    
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('event_name','full_name', 'company_name','event_status')
    list_filter = ('event_status', 'contract_id__client_id__last_name', 'contract_id__client_id__email' )
    search_fields = ['event_date', 'contract_id__client_id__last_name', 'contract_id__client_id__email' ]


    def full_name(self, instance):
        return f"{instance.contract_id.client_id.last_name.upper()}  {instance.contract_id.client_id.first_name.capitalize()}"
    
    full_name.short_description = "Client"
    full_name.admin_order_field = "client_id__last_name"
    
    def event_name(self, instance):
        return f"{instance.contract_id.name.capitalize()}"
    
    event_name.short_description = "Nom"

    def company_name(self, instance):
        return f"{instance.contract_id.client_id.company_name.upper()}"
    
    company_name.short_description = "Société"
    company_name.admin_order_field = "contract_id__client_id__company_name"
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "support_contact_id":
            kwargs["queryset"] = Employee.objects.filter(groups__name__in=['Management', 'Support']) 
        
        add_view = request.path.split("/")[-2]
        if db_field.name == "contract_id" and add_view == 'add':
            kwargs["queryset"] = Contract.objects.filter(status=True).exclude(name__in=Event.objects.all().values_list('contract_id__name'))


        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj = None, ** kwargs)
        is_superuser = request.user.is_superuser
        
        if kwargs['change'] == True and len(form.base_fields) > 0:
            form.base_fields["contract_id"].disabled = True
            if not is_superuser:
                form.base_fields["support_contact_id"].disabled = True
            
        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:  # type: ignore
            return qs
        return qs.filter(contract_id__client_id__sales_contact_id=request.user) | qs.filter(support_contact_id=request.user)
    

crm_site.register(EventStatus)
crm_site.register(Event, EventAdmin)

