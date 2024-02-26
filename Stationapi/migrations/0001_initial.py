# Generated by Django 4.2.4 on 2024-02-21 10:19

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_name', models.CharField(max_length=200, null=True)),
                ('train_number', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('Non AC', 'Non AC'), ('AC', 'AC'), ('AC-2-tier', 'AC-2-tier'), ('AC-3-tier', 'AC-3-tier'), ('Sleeper', 'Sleeper')], default='AC', max_length=200)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('station', 'station'), ('Customer', 'Customer')], default='station', max_length=50)),
                ('phone', models.CharField(max_length=10, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('email_address', models.EmailField(max_length=254)),
                ('biodata', models.ImageField(upload_to='images')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('Stationapi.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=255)),
                ('station_code', models.CharField(max_length=100, null=True)),
                ('Location', models.CharField(max_length=200, null=True)),
                ('phone_number', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('Stationapi.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('reserved_seats', models.IntegerField(default=1)),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('Starting_From', models.CharField(max_length=200, null=True)),
                ('Going_To', models.CharField(max_length=200)),
                ('payment', models.PositiveIntegerField()),
                ('is_confirmed', models.BooleanField(default=False)),
                ('train_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stationapi.train')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stationapi.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_id', models.CharField(max_length=20)),
                ('distance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ending_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ending_routes', to='Stationapi.station')),
                ('intermediate_stops', models.ManyToManyField(blank=True, related_name='route_stops', to='Stationapi.station')),
                ('starting_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='starting_routes', to='Stationapi.station')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comments', models.TextField()),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stationapi.train')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stationapi.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Cancellation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancellation_date', models.DateTimeField(auto_now_add=True)),
                ('reason', models.TextField()),
                ('reservation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Stationapi.booking')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stationapi.customer')),
            ],
        ),
    ]