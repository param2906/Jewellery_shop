# Generated by Django 3.2.6 on 2021-10-24 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_jewellery_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]
