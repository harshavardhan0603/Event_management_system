# Generated by Django 4.1.4 on 2023-01-05 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_name', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('charges', models.IntegerField()),
                ('image', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='booking_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='booking_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_name', models.CharField(max_length=100)),
                ('EventType', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('no_of_days', models.IntegerField()),
                ('breakfast', models.BooleanField(default=False)),
                ('lunch', models.BooleanField(default=False)),
                ('TeaSnacks', models.BooleanField(default=False)),
                ('dinner', models.BooleanField(default=False)),
                ('Nonveg', models.BooleanField(default=False)),
                ('NoofGuest', models.IntegerField()),
                ('Amount', models.IntegerField()),
                ('Decoration', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
