# Generated by Django 4.2.5 on 2023-10-30 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_remove_video_iframe_remove_video_video_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='discount',
            field=models.IntegerField(blank=0, default=0, help_text='discount is %, put 0 if it has no discount', null=True),
        ),
    ]
