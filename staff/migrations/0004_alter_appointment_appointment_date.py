# Generated by Django 5.0.2 on 2024-07-27 07:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_appointment_appointment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateField(default=datetime.datetime(2024, 7, 28, 7, 57, 44, 720724, tzinfo=datetime.timezone.utc)),
        ),
    ]
