# Generated by Django 3.0.2 on 2020-03-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_auto_20200316_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='homework',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='homework_attachment',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
