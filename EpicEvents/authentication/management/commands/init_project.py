from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from clients.models import Client, ClientStatus
from contracts.models import Contract
from events.models import Event, EventStatus

try:
    import init_config
except ImportError:
    raise ImportError('Veuiller configurer votre fichier init_config.py à la racine du projet')


UserModel = get_user_model()

GROUPS = [
    { 'name' : 'Sales', 
     'permissions': {
         'client': ['add', 'change', 'view'],
         'contract': ['add', 'change', 'view'],
         'event': ['view', 'add']
         }
     },
    { 'name' : 'Support', 
     'permissions':{
         'client': ['view'],
         'event': ['add', 'change', 'view']
        }
     },
    { 'name' : 'Management', 'permissions': 'all'}
]


ADMIN_ID = init_config.ADMIN_ID
ADMIN_PASSWORD = init_config.ADMIN_PASSWORD
ADMIN_FIRST_NAME = init_config.ADMIN_FIRST_NAME
ADMIN_LAST_NAME = init_config.ADMIN_LAST_NAME


class Command(BaseCommand):
    
    init_msg = "Initialisation du projet"
    db_delete_msg = "Effacement des tables"
    group_create_msg = "initialisation de la table groupe"
    superuser_create_msg = "Initialisation de l'administrateur"
    create_done_msg = "Terminé"
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        self.stdout.write(self.style.MIGRATE_HEADING(self.db_delete_msg))
        
        Event.objects.all().delete()
        EventStatus.objects.all().delete()
        Contract.objects.all().delete()
        Client.objects.all().delete()
        ClientStatus.objects.all().delete()
        UserModel.objects.all().delete()
        Group.objects.all().delete()
        
        self.stdout.write(self.style.MIGRATE_HEADING(self.group_create_msg))
        
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
        
        self.stdout.write(self.style.SUCCESS(self.create_done_msg))
        self.stdout.write(self.style.MIGRATE_HEADING(self.superuser_create_msg))

        UserModel.objects.create_superuser(
            email=ADMIN_ID,
            password=ADMIN_PASSWORD,
            first_name=ADMIN_FIRST_NAME,
            last_name=ADMIN_LAST_NAME
            )
            
        self.stdout.write(self.style.SUCCESS(self.create_done_msg))
        self.stdout.write(self.style.SUCCESS("Le projet est prêt !"))
 