from asyncio import events
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from authentication.models import Employee
from clients.models import Client, ClientStatus
from contracts.models import Contract
from events.models import Event, EventStatus
from datetime import date


UserModel = get_user_model()

GROUPS = [
    { 'name' : 'Sales', 
     'permissions': {
         'client': ['add', 'change', 'delete', 'view'],
         'contract': ['add', 'change', 'delete', 'view'],
         'event': ['view']
         }
     },
    { 'name' : 'Support', 
     'permissions':{
         'client': ['view'],
         'contract': ['view'],
         'event': ['add', 'change', 'delete', 'view']
        }
     },
    { 'name' : 'Management', 'permissions': 'all'}
]

EMPLOYEES = [
    {
        'first_name': "Pierre",
        'last_name': "Jean",
        'email': "pierre.jean@gmail.com",
        'phone': "0102030405",
        'mobile': "0601020304",
        'password': "S3cr3tW0rd",
        'group': 'Sales'
    },
    {
        'first_name': "Paul",
        'last_name': "Jacques",
        'email': "paul.jacques@gmail.com",
        'phone': "0506070809",
        'mobile': "0605060708",
        'password': "S3cr3tW0rd",
        'group': 'Support'
    }
]

CLIENT_STATUS = [
    {
        'status': 'Client',
    },
    {
        'status': 'Prospect',
    }
]

CLIENTS = [
    {
        'first_name': "Bill",
        'last_name': "Malone",
        'email': "bill.Malone@gmail.com",
        'phone': "0102030405",
        'mobile': "0601020304",
        'company_name': "Test Corporation",
        'sales_contact_id': "pierre.jean@gmail.com",
        'status': "Prospect",
    },
    {
        'first_name': "Tom",
        'last_name': "Marc",
        'email': "tom.marc@gmail.com",
        'phone': "0102030405",
        'mobile': "0601020304",
        'company_name': "Test institut",
        'sales_contact_id': "pierre.jean@gmail.com",
        'status': 'Client',
    }

]

CONTRACTS = [
    {
        'payment_due': date.today(),
        'amount_float': 30000.40,
        'client_id': "bill.Malone@gmail.com",
        'name': 'Fête de la bière'
    }
]

EVENTS_STATUS = [
    {
        'status': "En préparation"
    },
    {
        'status': "En Cours"
    },
    {
        'status': "Terminé"
    }
]

EVENTS = [
    {
        'event_date': date.today(),
        'attendees': 1500,
        'contract_id': 'Fête de la bière' ,
        'event_status': 'En préparation',
        'support_contact_id': 'paul.jacques@gmail.com'
    }
]


ADMIN_ID = 'admin@epic.com'
ADMIN_PASSWORD = 'Azerty01'
ADMIN_FIRST_NAME = 'Admin'
ADMIN_LAST_NAME = 'EPIC'


class Command(BaseCommand):
    
    help = "Initialize demo's data"
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        
        Event.objects.all().delete()
        EventStatus.objects.all().delete()
        Contract.objects.all().delete()
        Client.objects.all().delete()
        ClientStatus.objects.all().delete()
        UserModel.objects.all().delete()
        Group.objects.all().delete()
        
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
                        except:
                            continue
                group.permissions.set(group_perms)
                
        for data_employee in EMPLOYEES:
            employee = Employee.objects.create_user(
                    first_name = data_employee['first_name'],
                    last_name = data_employee['last_name'],
                    email = data_employee['email'],
                    phone = data_employee['phone'],
                    mobile = data_employee['mobile'],
                    password = data_employee['password'],
                )
            employee_group = Group.objects.get(name=data_employee['group'])
            employee_group.user_set.add(employee.id)
            
            
        for data_client_status in CLIENT_STATUS:
            ClientStatus.objects.create(
                status = data_client_status['status']
            )
            
        for data_client in CLIENTS:
            Client.objects.create(
                first_name =  data_client['first_name'],
                last_name = data_client['last_name'],
                email =  data_client['email'],
                phone = data_client['phone'],
                mobile =  data_client['mobile'],
                company_name = data_client['company_name'],
                sales_contact_id = Employee.objects.get(email=data_client['sales_contact_id']),
                status = ClientStatus.objects.get(status=data_client['status'])
            )
            
        for data_contracts in CONTRACTS:
            Contract.objects.create(
                payment_due = data_contracts['payment_due'],
                amount_float = data_contracts['amount_float'],
                client_id = Client.objects.get(email=data_contracts['client_id']),
                name = data_contracts['name'],
            )
        
        for data_event_status in EVENTS_STATUS:
            EventStatus.objects.create(
                status = data_event_status['status']
            )
        
        for data_event in EVENTS:
            Event.objects.create(
                event_date = data_event['event_date'],
                attendees = data_event['attendees'],
                contract_id = Contract.objects.get(name=data_event['contract_id']),
                event_status = EventStatus.objects.get(status=data_event['event_status']),
                support_contact_id = Employee.objects.get(email=data_event['support_contact_id'])
            )
        
        UserModel.objects.create_superuser(
            email=ADMIN_ID,
            password=ADMIN_PASSWORD,
            first_name=ADMIN_FIRST_NAME,
            last_name=ADMIN_LAST_NAME
            )
            
        self.stdout.write(self.style.SUCCESS("All Done !"))
        

        