# Generated by Django 2.1.7 on 2019-03-06 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_auto_20190304_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='unit',
            field=models.CharField(default='fahrenheit', max_length=50),
        ),
    ]
