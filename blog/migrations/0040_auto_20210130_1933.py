# Generated by Django 3.1.5 on 2021-01-30 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0039_auto_20210130_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesettings',
            name='map_latitude',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='map_longitude',
        ),
    ]
