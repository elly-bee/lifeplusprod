# Generated by Django 5.0.6 on 2024-09-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_myuser_usercode_transaction_bonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus_tran',
            name='rundate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]