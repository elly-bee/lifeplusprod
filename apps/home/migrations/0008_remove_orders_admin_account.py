# Generated by Django 5.0.6 on 2024-09-21 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_orders_admin_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='admin_account',
        ),
    ]
