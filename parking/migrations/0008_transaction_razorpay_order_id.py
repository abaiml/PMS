# Generated by Django 5.0.7 on 2024-09-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0007_booking_plate_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
