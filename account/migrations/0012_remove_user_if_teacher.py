# Generated by Django 3.0.7 on 2020-06-18 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20200618_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='if_teacher',
        ),
    ]
