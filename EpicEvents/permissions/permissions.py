from operator import truediv
from rest_framework.permissions import BasePermission
from authentication.models import Employee
from django.contrib.auth.models import Group


class HasGroupPerms(BasePermission):
    def has_permission(self, request, view):
        
        perms_map = {
            'create' : 'add',
            'list': 'view',
            'retrieve': 'view',
            'destroy': 'delete',
            'update': 'change'
        }
        
        perms_group_lst = []
        action_perm = perms_map.get(view.action, 'no')
        perm_required = f"{action_perm}_{view.basename}"
        employee_groups=request.user.groups.values_list('name', flat=True)
        for employee_group in employee_groups:
            group_obj=Group.objects.get(name=employee_group)
            employee_perms_group= group_obj.permissions.values_list('codename', flat=True)
            for perm_group_name in employee_perms_group:
                perms_group_lst.append(perm_group_name)
        if perm_required in perms_group_lst:
            return True
        else:
            return False

    