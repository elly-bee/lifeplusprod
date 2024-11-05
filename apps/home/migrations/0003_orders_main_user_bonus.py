# Generated by Django 5.0.6 on 2024-09-14 05:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_orders_main_user_alter_myuser_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='main_user_bonus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_bonus', to=settings.AUTH_USER_MODEL),
        ),
    ]