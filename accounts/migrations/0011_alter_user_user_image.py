# Generated by Django 4.2.5 on 2023-10-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_user_is_instructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(default='media/users/user.png', null=True, upload_to='media/users/'),
        ),
    ]
