# Generated by Django 5.1.4 on 2025-03-25 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0007_booking_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='booking_date',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='booking',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
