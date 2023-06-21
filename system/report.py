from .models import Child



def generate_report():
    # Retrieve all children with their associated appointments and vaccines
    children = Child.objects.all().prefetch_related('appointments__vaccines')

    # Start building the report string
    report = "Report\n\n"

    for child in children:
        report += f"Child: {child.first_name} {child.last_name}\n"

        # Check if the child has a vaccine assigned
        if child.vaccine:
            report += f"Assigned Vaccine: {child.vaccine.name}\n"

        # Loop through the child's appointments
        for appointment in child.appointments.all():
            report += f"Appointment Date: {appointment.date}\n"
            report += f"Doctor: {appointment.doctor.first_name} {appointment.doctor.last_name}\n"

            # Check if the appointment has any associated vaccines
            if appointment.vaccines.exists():
                report += "Vaccines:\n"
                for vaccine in appointment.vaccines.all():
                    report += f"- {vaccine.name}\n"

            report += "\n"

        report += "--------------------------\n\n"

    return report
