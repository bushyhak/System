# Generated by Django 4.2.1 on 2023-06-24 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0032_remove_appointment_administered_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministeredVaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_administered', models.DateField()),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='administered_vaccines', to='system.child')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.vaccines')),
            ],
        ),
    ]
