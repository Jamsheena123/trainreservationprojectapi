# Generated by Django 4.2.4 on 2024-02-26 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0011_remove_booking_going_to_remove_booking_starting_from'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='is_confirmed',
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=100),
        ),
    ]
