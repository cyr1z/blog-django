# Generated by Django 3.1.5 on 2021-01-29 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_auto_20210129_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='post',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='album', to='blog.post'),
        ),
    ]
