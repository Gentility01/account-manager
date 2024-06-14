# Generated by Django 4.2.11 on 2024-06-12 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='deal_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='deal_of_the_week',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='deal_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
