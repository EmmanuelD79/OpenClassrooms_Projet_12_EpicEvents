from django.contrib import admin
from authentication.models import Employee
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm, AdminPasswordChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin


class CrmAdminArea(admin.AdminSite):
    site_header = 'EPIC EVENTS CRM'


crm_site = CrmAdminArea(name='CrmAdmin')


class EmployeeAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('full_name', 'email', 'phone', 'mobile')
    list_filter = ()
    search_fields = ['first_name', 'last_name']
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Details Employee',
         {'fields': ('first_name', 'last_name', 'phone', 'mobile')}),
        ('Info', {'fields': ('date_created', 'date_updated', 'groups', 'is_staff', 'is_superuser')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Info', {
            'fields': (('first_name', 'last_name'), ('phone', 'mobile'))
        }),
        ('Permissions', {
            'fields': (('is_staff', 'is_superuser'), 'groups')}),
    )

    def full_name(self, instance):
        return f"{instance.last_name.upper()}  {instance.first_name.capitalize()}"

    full_name.short_description = "Employée"
    full_name.admin_order_field = "last_name"


crm_site.register(Group)

crm_site.register(Employee, EmployeeAdmin)
