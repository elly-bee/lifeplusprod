# Generated by Django 5.0.6 on 2024-10-03 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_orders_admin_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='points',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
