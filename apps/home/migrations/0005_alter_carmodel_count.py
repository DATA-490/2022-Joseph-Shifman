# Generated by Django 3.2.13 on 2022-10-28 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_carmodel_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='count',
            field=models.IntegerField(verbose_name='Number of recalls'),
        ),
    ]
