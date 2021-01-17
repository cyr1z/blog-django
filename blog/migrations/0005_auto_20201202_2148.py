# Generated by Django 3.1.3 on 2020-12-02 21:48

from django.db import migrations
import markdownfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201202_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text_rendered',
            field=markdownfield.models.RenderedMarkdownField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=markdownfield.models.MarkdownField(default=1, rendered_field='text_rendered'),
            preserve_default=False,
        ),
    ]