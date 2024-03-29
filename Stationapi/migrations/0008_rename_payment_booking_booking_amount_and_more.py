# Generated by Django 4.2.4 on 2024-02-26 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0007_remove_train_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='payment',
            new_name='booking_amount',
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
    ]
