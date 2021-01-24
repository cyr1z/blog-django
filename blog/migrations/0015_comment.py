# Generated by Django 3.1.3 on 2021-01-16 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField(blank=True, max_length=1000, null=True, verbose_name='text')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='blog.post')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post Comment',
                'verbose_name_plural': 'Post Comments',
                'ordering': ['created_at'],
            },
        ),
    ]