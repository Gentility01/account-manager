# Generated by Django 4.2.11 on 2024-05-08 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_alter_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='best_seller',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='newly_arrived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='special_offer',
            field=models.BooleanField(default=False),
        ),
    ]
