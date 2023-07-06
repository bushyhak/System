from django.core.management.base import BaseCommand
from system.models import Doctor


class Command(BaseCommand):
    help = "Loads some initial doctors into the database"

    def handle(self, *args, **options):
        # Dummy data for 10 doctors
        doctors = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "license_no": "12345",
                "available": True,
            },
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "license_no": "23456",
                "available": False,
            },
            {
                "first_name": "Bob",
                "last_name": "Smith",
                "license_no": "34567",
                "available": True,
            },
            {
                "first_name": "Alice",
                "last_name": "Jones",
                "license_no": "45678",
                "available": True,
            },
            {
                "first_name": "David",
                "last_name": "Lee",
                "license_no": "56789",
                "available": False,
            },
            {
                "first_name": "Sarah",
                "last_name": "Kim",
                "license_no": "67890",
                "available": True,
            },
            {
                "first_name": "Michael",
                "last_name": "Nguyen",
                "license_no": "78901",
                "available": True,
            },
            {
                "first_name": "Jessica",
                "last_name": "Wong",
                "license_no": "89012",
                "available": True,
            },
            {
                "first_name": "William",
                "last_name": "Chen",
                "license_no": "90123",
                "available": False,
            },
            {
                "first_name": "Karen",
                "last_name": "Liu",
                "license_no": "01234",
                "available": True,
            },
        ]
        # Create the doctors in the database
        for doctor in doctors:
            Doctor.objects.create(**doctor)
        self.stdout.write(
            self.style.SUCCESS("Successfully loaded doctors into the database")
        )
