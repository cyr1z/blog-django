# Generated by Django 3.1.3 on 2021-01-22 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20210122_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='avatar_image',
            field=models.ImageField(blank=True, null=True, upload_to='users_images', verbose_name='Image'),
        ),
    ]
