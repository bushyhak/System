# Generated by Django 4.2.1 on 2023-07-11 19:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0010_alter_feedback_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created on'),
        ),
    ]
