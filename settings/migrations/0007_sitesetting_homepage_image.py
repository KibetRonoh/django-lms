# Generated by Django 4.2.5 on 2023-10-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_alter_sitesetting_banner_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='homepage_image',
            field=models.ImageField(default=0, upload_to='media/homepage/'),
        ),
    ]
