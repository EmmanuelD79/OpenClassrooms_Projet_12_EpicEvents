from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group, Permission
from authentication.models import Employee
from clients.models import Client, ClientStatus
from contracts.models import Contract
from events.models import Event, EventStatus
from .data import EMPLOYEES, CLIENTS, ADMIN_USER, EVENTS_STATUS, GROUPS, CLIENT_STATUS, CONTRACTS, EVENTS
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


def get_tokens_for_user(user):
    """
    Get refresh and access tokens for the request.user

    Args:
        user (Employee): Login user

    Returns:
        'refresh': Refresh token
        'access' : Access token
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class InitDb:
    """
    Use to init a dataset for tests and demo.
    """
    @staticmethod
    def _init_db_group():
        for data_group in GROUPS:
            group_perms = []
            group = Group.objects.create(name=data_group['name'])
            if data_group['permissions'] == 'all':
                all_permission = Permission.objects.all()
                group.permissions.set(all_permission)
            else:
                for data_perm in data_group['permissions']:
                    for data_auto in data_group['permissions'][data_perm]:
                        try:
                            perm_obj = Permission.objects.get(codename=f'{data_auto}_{data_perm}')
                            group_perms.append(perm_obj.id)
                        except ObjectDoesNotExist:
                            continue
                group.permissions.set(group_perms)

    @staticmethod
    def _init_db_employee():
        for data_employee in EMPLOYEES:
            employee = Employee.objects.create_user(
                    first_name=data_employee['first_name'],
                    last_name=data_employee['last_name'],
                    email=data_employee['email'],
                    phone=data_employee['phone'],
                    mobile=data_employee['mobile'],
                    password=data_employee['password'],
                )
            employee_group = Group.objects.get(name=data_employee['group'])
            employee_group.user_set.add(employee.id)

    @staticmethod
    def _init_db_client_status():
        for data_client_status in CLIENT_STATUS:
            ClientStatus.objects.create(
                status=data_client_status['status']
            )

    @staticmethod
    def _init_db_client():
        for data_client in CLIENTS:
            Client.objects.create(
                first_name=data_client['first_name'],
                last_name=data_client['last_name'],
                email=data_client['email'],
                phone=data_client['phone'],
                mobile=data_client['mobile'],
                company_name=data_client['company_name'],
                sales_contact_id=Employee.objects.get(email=data_client['sales_contact_id']),
                status=ClientStatus.objects.get(status=data_client['status'])
            )

    @staticmethod
    def _init_db_contracts():
        for data_contracts in CONTRACTS:
            Contract.objects.create(
                payment_due=data_contracts['payment_due'],
                amount_float=data_contracts['amount_float'],
                client_id=Client.objects.get(email=data_contracts['client_id']),
                status=data_contracts['status'],
                name=data_contracts['name'],
            )

    @staticmethod
    def _init_db_event_status():
        for data_event_status in EVENTS_STATUS:
            EventStatus.objects.create(
                status=data_event_status['status']
            )

    @staticmethod
    def _init_db_event():
        for data_event in EVENTS:
            Event.objects.create(
                event_date=data_event['event_date'],
                attendees=data_event['attendees'],
                contract_id=Contract.objects.get(name=data_event['contract_id']),
                event_status=EventStatus.objects.get(status=data_event['event_status']),
                support_contact_id=Employee.objects.get(email=data_event['support_contact_id'])
            )

    @classmethod
    def run(cls):
        """
        Create a complete dataset into database.
        """
        cls._init_db_group()
        cls._init_db_employee()
        cls._init_db_client_status()
        cls._init_db_client()
        cls._init_db_contracts()
        cls._init_db_event_status()
        cls._init_db_event()

    @classmethod
    def destroy_db(cls):
        """
        Delete all tables of database.
        """
        Event.objects.all().delete()
        EventStatus.objects.all().delete()
        Contract.objects.all().delete()
        Client.objects.all().delete()
        ClientStatus.objects.all().delete()
        Employee.objects.all().delete()
        Group.objects.all().delete()

    @classmethod
    def create_admin_user(cls):
        """
        Create an admin user as superuser.
        """
        admin_user = get_user_model()
        admin_user.objects.create_superuser(
            email=ADMIN_USER['email'],
            password=ADMIN_USER['password'],
            first_name=ADMIN_USER['first_name'],
            last_name=ADMIN_USER['last_name']
            )

    @classmethod
    def refresh_db(cls):
        """
        Refresh the database with the demo dataset.
        """
        cls.destroy_db()
        cls.run()

    @classmethod
    def create_groups_user(cls):
        """
        Create all groups : "Management", "Sales" and "Support" into database.
        """
        cls._init_db_group()

    @classmethod
    def run_dataset(cls):
        """
        Create a demo dataset into database.
        """
        Event.objects.all().delete()
        EventStatus.objects.all().delete()
        Contract.objects.all().delete()
        Client.objects.all().delete()
        ClientStatus.objects.all().delete()

        cls._init_db_employee()
        cls._init_db_client_status()
        cls._init_db_client()
        cls._init_db_contracts()
        cls._init_db_event_status()
        cls._init_db_event()
