# Generated by Django 4.2.5 on 2023-10-24 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_sitesetting_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='google_map_location',
            field=models.CharField(default='o', max_length=1000),
        ),
    ]
