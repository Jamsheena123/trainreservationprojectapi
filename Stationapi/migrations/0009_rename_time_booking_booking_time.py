# Generated by Django 4.2.4 on 2024-02-26 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0008_rename_payment_booking_booking_amount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='time',
            new_name='booking_time',
        ),
    ]
