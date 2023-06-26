from django.core.management.base import BaseCommand
from system import models
from system.models import Vaccines

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        duplicate_vaccines = Vaccines.objects.values('name').annotate(count=models.Count('name')).filter(count__gt=1)
        
        for vaccine in duplicate_vaccines:
            vaccine_name = vaccine['name']
            duplicate_records = Vaccines.objects.filter(name=vaccine_name)
            
            # Keep the first occurrence of the vaccine
            duplicate_records.exclude(pk=duplicate_records.first().pk).delete()
            
        self.stdout.write(self.style.SUCCESS('Duplicate records removed successfully.'))
