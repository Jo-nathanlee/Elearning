# Generated by Django 3.0.2 on 2020-09-10 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0023_homework_if_share'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='homework_url',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]