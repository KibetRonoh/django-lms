# Generated by Django 4.2.5 on 2023-10-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(null=True, upload_to='media/users/'),
        ),
    ]