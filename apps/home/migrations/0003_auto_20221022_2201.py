# Generated by Django 3.2.13 on 2022-10-22 22:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_alter_carmodel_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='carmodel',
            unique_together={('user', 'year', 'make', 'model')},
        ),
        migrations.RemoveField(
            model_name='carmodel',
            name='trim',
        ),
    ]
