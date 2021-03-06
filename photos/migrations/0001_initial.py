# Generated by Django 2.1.3 on 2019-02-16 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0005_moduletype_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(default='default_bg.jpg', upload_to='background_pics')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Module')),
            ],
        ),
    ]
