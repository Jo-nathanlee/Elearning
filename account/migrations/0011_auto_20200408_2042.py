# Generated by Django 3.0.2 on 2020-04-08 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20200408_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
