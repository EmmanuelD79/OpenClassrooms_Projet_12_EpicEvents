from django.core.management.base import BaseCommand
from utils.utils import InitDb


class Command(BaseCommand):

    init_msg = "Initialisation du projet"
    db_delete_msg = "Effacement des tables"
    group_create_msg = "initialisation de la table groupe"
    superuser_create_msg = "Initialisation de l'administrateur"
    create_done_msg = "Terminé"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        self.stdout.write(self.style.MIGRATE_HEADING(self.db_delete_msg))

        InitDb.destroy_db()

        self.stdout.write(self.style.MIGRATE_HEADING(self.group_create_msg))

        InitDb.create_groups_user()

        self.stdout.write(self.style.SUCCESS(self.create_done_msg))
        self.stdout.write(self.style.MIGRATE_HEADING(self.superuser_create_msg))

        InitDb.create_admin_user()

        self.stdout.write(self.style.SUCCESS(self.create_done_msg))
        self.stdout.write(self.style.SUCCESS("Le projet est prêt !"))
