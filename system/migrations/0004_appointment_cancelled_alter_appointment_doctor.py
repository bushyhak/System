# Generated by Django 4.2.1 on 2023-07-06 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_appointment_completed_doctor_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='system.doctor'),
        ),
    ]
