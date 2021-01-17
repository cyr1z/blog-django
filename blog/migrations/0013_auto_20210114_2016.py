# Generated by Django 3.1.3 on 2021-01-14 20:16

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_bloguser_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='full_name'),
        ),
    ]