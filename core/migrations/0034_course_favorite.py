# Generated by Django 4.2.5 on 2023-10-26 13:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0033_alter_course_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='favorite',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]
