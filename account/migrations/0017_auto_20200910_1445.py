# Generated by Django 3.0.2 on 2020-09-10 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_remove_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='self_introduction',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]