# Generated by Django 3.0.7 on 2020-08-03 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0020_homework_homework_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='note',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
