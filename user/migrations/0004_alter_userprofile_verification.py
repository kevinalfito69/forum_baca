# Generated by Django 4.1.1 on 2024-01-16 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_userprofile_verification_delete_verificationuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='verification',
            field=models.BooleanField(default=False),
        ),
    ]