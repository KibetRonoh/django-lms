# Generated by Django 4.2.5 on 2023-10-24 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_sitesetting_google_map_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetting',
            name='google_map_location',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]