from django.contrib import admin
from .models import Event, EventStatus
from authentication.admin import crm_site
from django.contrib import messages


class EventStatusAdmin(admin.ModelAdmin):
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

class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details Event',
         {'fields': ('full_name', 'company_name', 'event_status')}),
        ('Info', {'fields': ('support_contact_id', 'event_date', 'attendees', 'date_created', 'date_updated')})
    )
    
    readonly_fields = ('full_name', 'company_name', 'date_created', 'date_updated')
    list_display = ('id', 'full_name', 'company_name', 'event_status')
    list_filter = ('client_id__company_name', 'event_status', 'support_contact_id__email')
    search_fields = ['event_date', 'attendees']

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
        
        return True

    def has_change_permission(self, request, obj=None):
        
        if request.user.is_superuser:
            return True
        
        return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        
        return True
   
    
crm_site.register(EventStatus, EventStatusAdmin)
crm_site.register(Event, EventAdmin)

