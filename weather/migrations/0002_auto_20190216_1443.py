# Generated by Django 2.1.3 on 2019-02-16 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='forecast_length',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='weather',
            name='show_forecast',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
