# Generated by Django 4.2.4 on 2023-09-17 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_account_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile/images.jpeg', null=True, upload_to='profile/'),
        ),
    ]
