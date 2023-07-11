# Generated by Django 4.2.1 on 2023-07-10 10:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_delete_customlogentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='first_name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only alphabetical characters are allowed')]),
        ),
    ]
