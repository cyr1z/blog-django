# Generated by Django 3.1.5 on 2021-01-30 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_auto_20210130_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesettings',
            name='map_coordinates',
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='map_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='map_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Coords',
        ),
    ]
