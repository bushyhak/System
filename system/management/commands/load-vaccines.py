from django.core.management.base import BaseCommand
from system.models import Vaccines


class Command(BaseCommand):
    help = "Loads some initial vaccines into the database"

    def handle(self, *args, **kwargs):
        vaccines = [
            {
                "name": "BCG",
                "weeks_minimum_age": 0,
                "weeks_maximum_age": 0,
            },
            {
                "name": "Hepatitis B Birth Dose",
                "weeks_minimum_age": 0,
                "weeks_maximum_age": 0,
            },
            {
                "name": "Polio Birth Dose",
                "weeks_minimum_age": 0,
                "weeks_maximum_age": 0,
            },
            {
                "name": "DPT Birth Dose",
                "weeks_minimum_age": 0,
                "weeks_maximum_age": 0,
            },
            {
                "name": "Hib 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 6,
            },
            {
                "name": "Polio 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 6,
            },
            {
                "name": "DPT 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 6,
            },
            {
                "name": "Rotavirus 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 6,
            },
            {
                "name": "PCV 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 6,
            },
            {
                "name": "Hepatitis B 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 6,
            },
            {
                "name": "Hib 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 10,
            },
            {
                "name": "Polio 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 10,
            },
            {
                "name": "DPT 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 10,
            },
            {
                "name": "Rotavirus 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 10,
            },
            {
                "name": "PCV 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 10,
            },
            {
                "name": "Hepatitis B 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 10,
            },
            {
                "name": "Hib 14 Weeks Dose",
                "weeks_minimum_age": 14,
                "weeks_maximum_age": 14,
            },
            {
                "name": "Polio 14 Weeks Dose",
                "weeks_minimum_age": 14,
                "weeks_maximum_age": 14,
            },
            {
                "name": "DPT 14 Weeks Dose",
                "weeks_minimum_age": 14,
                "weeks_maximum_age": 14,
            },
            {
                "name": "PCV 14 Weeks Dose",
                "weeks_minimum_age": 14,
                "weeks_maximum_age": 14,
            },
            {
                "name": "MMR 9 Months Dose",
                "weeks_minimum_age": 36,
                "weeks_maximum_age": 36,
            },
            {
                "name": "Chickenpox 12 Months Dose",
                "weeks_minimum_age": 48,
                "weeks_maximum_age": 48,
            },
            {
                "name": "HPV 10-14 Years Dose 1",
                "weeks_minimum_age": 120,
                "weeks_maximum_age": 168,
            },
        ]

        for vaccine in vaccines:
            Vaccines.objects.create(**vaccine)
        self.stdout.write(
            self.style.SUCCESS("Successfully loaded vaccines into the database")
        )
