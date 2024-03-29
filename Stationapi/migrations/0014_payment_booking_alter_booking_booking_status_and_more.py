# Generated by Django 4.2.4 on 2024-02-26 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0013_alter_booking_reserved_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='booking',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Stationapi.booking'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Stationapi.customer'),
        ),
    ]
