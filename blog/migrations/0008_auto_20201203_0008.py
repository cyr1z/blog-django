# Generated by Django 3.1.3 on 2020-12-03 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20201203_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='tag_posts', to='blog.Tag'),
        ),
    ]
