# Generated by Django 4.2.1 on 2023-07-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_alter_child_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
    ]