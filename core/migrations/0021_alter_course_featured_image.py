# Generated by Django 4.2.5 on 2023-10-21 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_course_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='featured_image',
            field=models.ImageField(help_text='Recommended Dimensions: 1000 x 600', null=True, upload_to='media/featured_image'),
        ),
    ]
