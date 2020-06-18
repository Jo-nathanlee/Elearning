# Generated by Django 3.0.7 on 2020-06-18 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_auto_20200506_2137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'permissions': (('can_access', 'can create update delete'),)},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='homework_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
