# Generated by Django 5.0.7 on 2024-08-23 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0006_remove_booking_customer_phone_booking_customer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='plate_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
