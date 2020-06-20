# Generated by Django 3.0.7 on 2020-06-20 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0015_auto_20200618_2113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homework',
            old_name='lesson_id',
            new_name='lesson',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='lesson_id',
            new_name='lesson',
        ),
        migrations.RemoveField(
            model_name='course',
            name='credits',
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]