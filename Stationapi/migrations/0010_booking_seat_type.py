# Generated by Django 4.2.4 on 2024-02-26 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0009_rename_time_booking_booking_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='seat_type',
            field=models.CharField(choices=[('Non AC', 'Non AC'), ('AC', 'AC'), ('Sleeper', 'Sleeper')], default='Sleeper', max_length=100),
        ),
    ]
