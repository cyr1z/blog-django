# Generated by Django 3.1.5 on 2021-01-29 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_delete_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='description',
        ),
        migrations.RemoveField(
            model_name='album',
            name='tags',
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tag_posts', to='blog.Tag'),
        ),
    ]
