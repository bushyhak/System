# Generated by Django 4.2.1 on 2023-06-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0038_appointment_status_alter_vaccines_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='Pending', max_length=50),
        ),
    ]