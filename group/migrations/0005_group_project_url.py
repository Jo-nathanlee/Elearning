# Generated by Django 3.0.7 on 2020-08-18 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_auto_20200731_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='project_url',
            field=models.TextField(default=''),
        ),
    ]
