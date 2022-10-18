from django.contrib import messages


class AdminPermissions:
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
