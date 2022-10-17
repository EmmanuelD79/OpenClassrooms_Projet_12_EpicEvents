from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authentication.models import Employee, Group
from clients.models import Client, ClientStatus

UserModel = get_user_model()

GROUPS = [
    { 'name' : 'Sales'},
    { 'name' : 'Support'},
    { 'name' : 'Management'}
]

EMPLOYEES = [
    {
        'first_name': "Pierre",
        'last_name': "Jean",
        'email': "pierre.jean@gmail.com",
        'phone': "0102030405",
        'mobile': "0601020304",
        'password': "S3cr3tW0rd",
        'group_name': 'Sales',
    },
    {
        'first_name': "Paul",
        'last_name': "Jacques",
        'email': "paul.jacques@gmail.com",
        'phone': "0506070809",
        'mobile': "0605060708",
        'password': "S3cr3tW0rd",
        'group_name': 'Support',
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

ADMIN_ID = 'admin@epic.com'
ADMIN_PASSWORD = 'Azerty01'
ADMIN_FIRST_NAME = 'Admin'
ADMIN_LAST_NAME = 'EPIC'


class Command(BaseCommand):
    
    help = "Initialize demo's data"
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        
        UserModel.objects.all().delete()
        Group.objects.all().delete()
        Client.objects.all().delete()
        ClientStatus.objects.all().delete()
        
        for data_group in GROUPS:
            Group.objects.create(name=data_group['name'])
        
        for data_employee in EMPLOYEES:
            Employee.objects.create_user(
                    first_name = data_employee['first_name'],
                    last_name = data_employee['last_name'],
                    email = data_employee['email'],
                    phone = data_employee['phone'],
                    mobile = data_employee['mobile'],
                    password = data_employee['password'],
                    group_name = Group.objects.get(pk=data_employee['group_name'])
                )
            
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
            
        
        UserModel.objects.create_superuser(
            email=ADMIN_ID,
            password=ADMIN_PASSWORD,
            first_name=ADMIN_FIRST_NAME,
            last_name=ADMIN_LAST_NAME
            )
            
        self.stdout.write(self.style.SUCCESS("All Done !"))
        

        