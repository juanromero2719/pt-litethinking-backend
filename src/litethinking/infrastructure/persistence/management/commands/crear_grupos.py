from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Crea los grupos de roles iniciales (Admin y Externo)'

    def handle(self, *args, **options):
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(
                self.style.SUCCESS('[OK] Grupo "Admin" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('[INFO] Grupo "Admin" ya existe')
            )

        externo_group, created = Group.objects.get_or_create(name='Externo')
        if created:
            self.stdout.write(
                self.style.SUCCESS('[OK] Grupo "Externo" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('[INFO] Grupo "Externo" ya existe')
            )

        self.stdout.write(
            self.style.SUCCESS('\n[OK] Proceso completado. Grupos listos para usar.')
        )

