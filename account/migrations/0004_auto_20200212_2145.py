# Generated by Django 3.0.2 on 2020-02-12 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_self_introduction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='pic_url',
        ),
        migrations.AddField(
            model_name='user',
            name='pic',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
