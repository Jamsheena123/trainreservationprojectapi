# Generated by Django 4.2.4 on 2024-03-14 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0020_remove_booking_seat_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train',
            name='seat_capacity',
        ),
        migrations.CreateModel(
            name='TrainCapacity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_seats', models.PositiveIntegerField(default=100)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stationapi.train')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='capacity', to='Stationapi.customer')),
            ],
        ),
    ]
