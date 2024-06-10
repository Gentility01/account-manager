# Generated by Django 4.2.11 on 2024-05-31 03:25

import auto_prefetch
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', auto_prefetch.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_profiles', to='users.account', verbose_name='Account')),
                ('user', auto_prefetch.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_profiles', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
                'base_manager_name': 'prefetch_manager',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('prefetch_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]