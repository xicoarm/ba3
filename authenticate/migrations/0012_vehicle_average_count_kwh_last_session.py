# Generated by Django 4.1.2 on 2022-10-25 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0011_rename_count_kw_vehicle_average_count_kw_last_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='average_count_kwh_last_session',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
