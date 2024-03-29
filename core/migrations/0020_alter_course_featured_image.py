# Generated by Django 4.2.5 on 2023-10-21 17:23

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_remove_course_user_alter_course_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='featured_image',
            field=models.ImageField(help_text='This is good', null=True, upload_to='media/featured_image', validators=[core.models.validate_image]),
        ),
    ]
