# Generated by Django 4.2.5 on 2024-05-08 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0030_rename_train_traincapacity_train_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traincapacity',
            old_name='train_number',
            new_name='train',
        ),
    ]
