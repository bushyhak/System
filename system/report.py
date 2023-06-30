from .models import Child


def generate_report():
    children = Child.objects.all().prefetch_related("appointments__vaccines")

    report = "Report\n\n"

    for child in children:
        report += f"Child: {child.first_name} {child.last_name}\n"

        if child.vaccine:
            report += f"Assigned Vaccine: {child.vaccine.name}\n"

        for appointment in child.appointments.all():
            report += f"Appointment Date: {appointment.date}\n"
            report += f"Doctor: {appointment.doctor.first_name} {appointment.doctor.last_name}\n"

            if appointment.vaccines.exists():
                report += "Vaccines:\n"
                for vaccine in appointment.vaccines.all():
                    report += f"- {vaccine.name}\n"

            report += "\n"

        report += "--------------------------\n\n"

    return report
