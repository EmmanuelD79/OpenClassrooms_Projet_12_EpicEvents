from rest_framework.permissions import IsAdminUser
from permissions.permissions import HasGroupPerms


class GetPermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'list', 'destroy', 'update', 'retrieve']:
            self.permission_classes = [HasGroupPerms]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
