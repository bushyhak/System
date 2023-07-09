from django.core.management.base import BaseCommand
from system.models import Vaccines


class Command(BaseCommand):
    help = "Deletes all vaccines from the database"

    def handle(self, *args, **kwargs):
        for vaccine in Vaccines.objects.all():
            vaccine.delete()
        self.stdout.write(
            self.style.SUCCESS("Successfully deleted all vaccines from the database")
        )
