# Generated by Django 4.2.1 on 2023-06-21 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0023_doctor_licence_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='licence_no',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
