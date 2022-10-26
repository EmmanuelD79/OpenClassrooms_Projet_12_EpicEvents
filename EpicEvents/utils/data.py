from datetime import date

try:
    from init_config import ADMIN_FIRST_NAME, ADMIN_ID, ADMIN_LAST_NAME, ADMIN_PASSWORD
except ImportError:
    raise ImportError('Veuiller configurer votre fichier init_config.py à la racine du projet')

GROUPS = [
    {'name': 'Sales',
     'permissions': {
         'client': ['add', 'change', 'view'],
         'contract': ['add', 'change', 'view'],
         'event': ['view', 'add']
         }
     },
    {'name': 'Support',
     'permissions': {
         'client': ['view'],
         'event': ['change', 'view']
        }
     },
    {'name': 'Management', 'permissions': 'all'}
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
        'status': 'Prospect',
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
        'client_id': CLIENTS[0]['email'],
        'status': True,
        'name': 'Fête de la bière'
    },
    {
        'payment_due': date.today(),
        'amount_float': 5000.40,
        'client_id': CLIENTS[1]['email'],
        'status': True,
        'name': 'La suprème'
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
        'contract_id': 'Fête de la bière',
        'event_status': 'En préparation',
        'support_contact_id': 'paul.jacques@gmail.com'
    }
]

NEW_EVENT = {
        'event_date': date.today(),
        'attendees': 3000,
        'contract_id': 'LA super_event',
        'event_status': 'En préparation',
        'support_contact_id': 'paul.jacques@gmail.com'
    }


NEW_CLIENT = {
        'first_name': "Tom",
        'last_name': "Pierre",
        'email': "tom.pierre@gmail.com",
        'phone': "0102030405",
        'mobile': "0601020304",
        'company_name': "Start",
        'status': 'Prospect',
    }


ADMIN_USER = {
    'email': ADMIN_ID,
    'password': ADMIN_PASSWORD,
    'first_name': ADMIN_FIRST_NAME,
    'last_name': ADMIN_LAST_NAME
}

NEW_CONTRACT = {
    'payment_due': date.today(),
    'amount_float': 1000.40,
    'status': True,
    'name': "L'evenement du siecle",
    }
