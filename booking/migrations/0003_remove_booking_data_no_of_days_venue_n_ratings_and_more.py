# Generated by Django 4.1.4 on 2023-01-07 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_booking_data_teasnacks_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_data',
            name='no_of_days',
        ),
        migrations.AddField(
            model_name='venue',
            name='n_ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='venue',
            name='ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='booking_data',
            name='Amount',
            field=models.IntegerField(default=0),
        ),
    ]
