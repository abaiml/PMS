# Generated by Django 5.0.7 on 2024-08-16 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0003_alter_booking_check_out_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(choices=[('entry', 'Entry'), ('exit', 'Exit')], max_length=5),
        ),
    ]
