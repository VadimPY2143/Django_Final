# Generated by Django 5.1.4 on 2024-12-25 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0002_rename_object_booking_object_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='object_id',
            new_name='object',
        ),
    ]
