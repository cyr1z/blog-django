# Generated by Django 3.1.3 on 2021-01-22 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20210118_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='avatar_image',
            field=models.ImageField(blank=True, default='avatar.png', null=True, upload_to='users_images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='static/category.png', null=True, upload_to='categories_images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='content',
            name='file',
            field=models.FileField(upload_to='contents_files'),
        ),
        migrations.AlterField(
            model_name='content',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='contents_files', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='preview',
            field=models.ImageField(blank=True, default='static/post.png', null=True, upload_to='posts_images', verbose_name='Image'),
        ),
    ]
