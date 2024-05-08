# Generated by Django 4.2.11 on 2024-05-08 10:42

import auto_prefetch
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_product_best_seller_product_newly_arrived_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='sub_category',
            field=auto_prefetch.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='ecommerce.category'),
        ),
    ]
