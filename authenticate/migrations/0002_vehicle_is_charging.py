# Generated by Django 4.1.2 on 2022-10-23 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='is_charging',
            field=models.BooleanField(default=False),
        ),
    ]
