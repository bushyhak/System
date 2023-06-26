# Generated by Django 4.2.1 on 2023-06-24 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0036_remove_vaccines_administered_vaccines_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='status',
        ),
        migrations.AlterField(
            model_name='vaccines',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
    ]