# Generated by Django 4.2.5 on 2024-05-08 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0029_alter_traincapacity_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traincapacity',
            old_name='train',
            new_name='train_number',
        ),
    ]
