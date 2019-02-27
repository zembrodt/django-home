# Generated by Django 2.1.3 on 2019-02-27 18:48

from django.db import migrations, models
import django.db.models.deletion
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_photos_is_background'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=photos.models.get_image_filename)),
            ],
        ),
        migrations.RemoveField(
            model_name='photos',
            name='image',
        ),
        migrations.AlterField(
            model_name='photos',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='dashboard.Module'),
        ),
        migrations.AddField(
            model_name='image',
            name='photos_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='photos.Photos'),
        ),
    ]
