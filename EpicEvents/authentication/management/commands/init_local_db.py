from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from utils.utils import InitDb


UserModel = get_user_model()

class Command(BaseCommand):
    
    help = "Initialize demo's data"
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        
        if UserModel.objects.count() > 1 or Group.objects.count() == 0:
            self.stdout.write(self.style.ERROR("Veuillez d'abord initialiser le projet avec la commande init_project"))
            quit()
                    
        InitDb.run_dataset()
        
        self.stdout.write(self.style.SUCCESS("All Done !"))
 