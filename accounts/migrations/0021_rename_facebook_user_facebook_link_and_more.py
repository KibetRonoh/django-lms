# Generated by Django 4.2.5 on 2023-10-30 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_user_facebook_user_instagram_user_x_user_youtube'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='facebook',
            new_name='facebook_link',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='instagram',
            new_name='instagram_link',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='x',
            new_name='x_link',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='youtube',
            new_name='youtube_link',
        ),
    ]
