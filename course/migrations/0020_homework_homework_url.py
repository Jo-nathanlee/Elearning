# Generated by Django 3.0.7 on 2020-08-03 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_auto_20200704_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='homework_url',
            field=models.TextField(default=''),
        ),
    ]
