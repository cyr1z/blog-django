# Generated by Django 3.1.5 on 2021-01-30 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_coords_sitesettings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesettings',
            options={'verbose_name': 'Site Settings', 'verbose_name_plural': 'Site Settings'},
        ),
    ]
