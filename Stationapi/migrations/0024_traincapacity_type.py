# Generated by Django 4.2.4 on 2024-03-15 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stationapi', '0023_alter_traincapacity_train'),
    ]

    operations = [
        migrations.AddField(
            model_name='traincapacity',
            name='type',
            field=models.CharField(choices=[('Non AC', 'Non AC'), ('AC', 'AC'), ('Sleeper', 'Sleeper')], max_length=100, null=True),
        ),
    ]
