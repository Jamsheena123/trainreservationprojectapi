# Generated by Django 4.2.4 on 2024-02-26 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0010_booking_seat_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='Going_To',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='Starting_From',
        ),
    ]