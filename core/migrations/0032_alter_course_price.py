# Generated by Django 4.2.5 on 2023-10-25 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_course_featured_as'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]