# Generated by Django 3.1.5 on 2021-01-30 13:03

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0038_auto_20210130_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='contact_about_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
