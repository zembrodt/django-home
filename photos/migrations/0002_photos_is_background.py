# Generated by Django 2.1.3 on 2019-02-27 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photos',
            name='is_background',
            field=models.BooleanField(default=False),
        ),
    ]