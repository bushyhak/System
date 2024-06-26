from django.core.management.base import BaseCommand
from system.models import Vaccines


class Command(BaseCommand):
    help = "Loads some initial vaccines into the database"

    def handle(self, *args, **kwargs):
        vaccines = [
            {
                "name": "BCG",
                "weeks_minimum_age": 0,
                "weeks_maximum_age": 2,
            },
            {
                "name": "Polio Birth Dose",
                "weeks_minimum_age": 0,
                "weeks_maximum_age": 2,
            },
            {
                "name": "Hib 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 7,
            },
            {
                "name": "Polio 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 7,
            },
            {
                "name": "DPT 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 7,
            },
            {
                "name": "Rotavirus 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 7,
            },
            {
                "name": "PCV 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 7,
            },
            {
                "name": "Hepatitis B 6 Weeks Dose",
                "weeks_minimum_age": 6,
                "weeks_maximum_age": 7,
            },
            {
                "name": "Hib 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 11,
            },
            {
                "name": "Polio 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 11,
            },
            {
                "name": "DPT 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 11,
            },
            {
                "name": "Rotavirus 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 11,
            },
            {
                "name": "PCV 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 11,
            },
            {
                "name": "Hepatitis B 10 Weeks Dose",
                "weeks_minimum_age": 10,
                "weeks_maximum_age": 11,
            },
            {
                "name": "Hib 14 Weeks Dose",
                "weeks_minimum_age": 14,
                "weeks_maximum_age": 15,
            },
            {
                "name": "Polio 14 Weeks Dose",
                "weeks_minimum_age": 14,
                "weeks_maximum_age": 15,
            },
            {
                "name": "DPT 14 Weeks Dose",
                "weeks_minimum_age": 14,
                "weeks_maximum_age": 15,
            },
            {
                "name": "PCV 14 Weeks Dose",
                "weeks_minimum_age": 14,
                "weeks_maximum_age": 15,
            },
            {
                "name": "Flu 28 Weeks Dose",
                "weeks_minimum_age": 28,
                "weeks_maximum_age": 29,
            },
            {
                "name": "MMR 9 Months Dose",
                "weeks_minimum_age": 36,
                "weeks_maximum_age": 37,
            },
            {
                "name": "Chickenpox 12 Months Dose",
                "weeks_minimum_age": 48,
                "weeks_maximum_age": 49,
            },
            {
                "name": "MMR 18 Months Dose",
                "weeks_minimum_age": 72,
                "weeks_maximum_age": 73,
            },
            {
                "name": "HPV 10 Years Dose",
                "weeks_minimum_age": 480,
                "weeks_maximum_age": 481,
            },
            {
                "name": "HPV 10 Years 6 Months Dose",
                "weeks_minimum_age": 504,
                "weeks_maximum_age": 505,
            },
        ]

        for vaccine in vaccines:
            Vaccines.objects.create(**vaccine)
        self.stdout.write(
            self.style.SUCCESS("Successfully loaded vaccines into the database")
        )
