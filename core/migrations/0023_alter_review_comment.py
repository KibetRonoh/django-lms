# Generated by Django 4.2.5 on 2023-10-22 19:49

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_course_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=tinymce.models.HTMLField(max_length=500, null=True),
        ),
    ]