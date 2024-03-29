# Generated by Django 4.1.1 on 2024-01-23 14:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0006_remove_userprofile_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='follower',
            field=models.ManyToManyField(related_name='user_follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(related_name='user_following', to=settings.AUTH_USER_MODEL),
        ),
    ]
