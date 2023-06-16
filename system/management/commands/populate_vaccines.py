from django.core.management.base import BaseCommand
from system.models import Vaccines

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        vaccines = [
            {
                'name': 'BCG',
                'minimum_age': 0,
                'maximum_age': 0,
            },
            {
                'name': 'Hepatitis B Birth Dose',
                'minimum_age': 0,
                'maximum_age': 0,
            },
            {
                'name': 'Hepatitis B 6 Weeks Dose',
                'minimum_age': 6,
                'maximum_age': 6,
            },
            {
                'name': 'Hepatitis B 10 Weeks Dose',
                'minimum_age': 10,
                'maximum_age': 10,
            },
            {
                'name': 'Polio Birth Dose',
                'minimum_age': 0,
                'maximum_age': 0,
            },
            {
                'name': 'Polio 6 Weeks Dose',
                'minimum_age': 6,
                'maximum_age': 6,
            },
            {
                'name': 'Polio 10 Weeks Dose',
                'minimum_age': 10,
                'maximum_age': 10,
            },
            {
                'name': 'Polio 14 Weeks Dose',
                'minimum_age': 14,
                'maximum_age': 14,
            },
            {
                'name': 'DPT Birth Dose',
                'minimum_age': 0,
                'maximum_age': 0,
            },
            {
                'name': 'DPT 6 Weeks Dose',
                'minimum_age': 6,
                'maximum_age': 6,
            },
            {
                'name': 'DPT 10 Weeks Dose',
                'minimum_age': 10,
                'maximum_age': 10,
            },
            {
                'name': 'DPT 14 Weeks Dose',
                'minimum_age': 14,
                'maximum_age': 14,
            },
            {
                'name': 'Hib 6 Weeks Dose',
                'minimum_age': 6,
                'maximum_age': 6,
            },
            {
                'name': 'Hib 10 Weeks Dose',
                'minimum_age': 10,
                'maximum_age': 10,
            },
            {
                'name': 'Hib 14 Weeks Dose',
                'minimum_age': 14,
                'maximum_age': 14,
            },
            {
                'name': 'Rotavirus 6 Weeks Dose',
                'minimum_age': 6,
                'maximum_age': 6,
            },
            {
                'name': 'Rotavirus 10 Weeks Dose',
                'minimum_age': 10,
                'maximum_age': 10,
            },
            {
                'name': 'PCV 6 Weeks Dose',
                'minimum_age': 6,
                'maximum_age': 6,
            },
            {
                'name': 'PCV 10 Weeks Dose',
                'minimum_age': 10,
                'maximum_age': 10,
            },
            {
                'name': 'PCV 14 Weeks Dose',
                'minimum_age': 14,
                'maximum_age': 14,
            },
            {
                'name': 'MMR 9 Months Dose',
                'minimum_age': 36,
                'maximum_age': 36,
            },
            {
                'name': 'Chickenpox 12 Months Dose',
                'minimum_age': 48,
                'maximum_age': 48,
            },
            {
                'name': 'HPV 10-14 Years Dose 1',
                'minimum_age': 120,
                'maximum_age': 168,
            },
        ]

        for vaccine in vaccines:
            Vaccines.objects.create(**vaccine)
