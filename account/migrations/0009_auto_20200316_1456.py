# Generated by Django 3.0.2 on 2020-03-16 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200312_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pic',
            field=models.TextField(blank=True, default='https://www.pinclipart.com/picdir/middle/8-82428_profile-clipart-generic-user-gender-neutral-head-icon.png', null=True),
        ),
    ]
