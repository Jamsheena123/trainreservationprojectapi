# Generated by Django 4.2.4 on 2024-03-19 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0027_train_station_alter_traincapacity_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stationapi.customer'),
        ),
    ]
