# Generated by Django 5.0.6 on 2024-08-21 08:57

import apps.home.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Occurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occurrence_type', models.CharField(choices=[('instant', 'Instant'), ('weekly', 'Weekly'), ('weekend', 'Weekend'), ('monthly', 'Monthly'), ('monthend', 'Month-End')], default='instant', max_length=10)),
            ],
            options={
                'verbose_name': 'Occurrence',
                'verbose_name_plural': 'Occurrences',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200, null=True)),
                ('special', models.CharField(default=apps.home.models.generate_custom_primary_key, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('usercode', models.CharField(max_length=8)),
                ('dateofbirth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('address', models.TextField(blank=True, max_length=250, null=True)),
                ('keyBonus', models.CharField(blank=True, max_length=150, null=True)),
                ('phone_number_1', models.CharField(blank=True, max_length=250, null=True)),
                ('phone_number_2', models.CharField(blank=True, max_length=250, null=True)),
                ('my_status', models.CharField(blank=True, choices=[('inactive', 'inactive'), ('renewal', 'incomplete'), ('active', 'renewal'), ('incomplete', 'active')], default='incomplete', max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='myuser_set', to='auth.group', verbose_name='groups')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='myuser_set_permissions', to='auth.permission', verbose_name='user permissions')),
                ('gender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.gender')),
                ('marital_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.maritalstatus')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('desc', models.CharField(blank=True, max_length=255, null=True)),
                ('transaction_type', models.IntegerField(choices=[(1, 'Credit'), (-1, 'Debit')], default=1)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('cur_bal', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=20, null=True)),
                ('acc_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('acc_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.acctype')),
            ],
        ),
        migrations.CreateModel(
            name='Product_bonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.CharField(max_length=50, null=True)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('occurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.occurance')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('package_name', models.CharField(max_length=20, null=True)),
                ('package_price', models.DecimalField(decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000000)])),
                ('bonus', models.ManyToManyField(to='home.product_bonus')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.products')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction_codes',
            fields=[
                ('tran_code', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_type', models.IntegerField(choices=[(1, 'Credit'), (-1, 'Debit')])),
                ('tran_bonus', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.product_bonus')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('desc', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('accType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.acctype')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.products')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tran_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.transaction_codes')),
            ],
        ),
        migrations.CreateModel(
            name='Bonus_tran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trandate', models.DateTimeField(auto_now_add=True)),
                ('rundate', models.DateTimeField()),
                ('status', models.CharField(choices=[('Processed', 'Processed'), ('Pending', 'Pending')], default='Pending', max_length=255)),
                ('acc_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.acctype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.orders')),
                ('tc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.transaction_codes')),
            ],
        ),
    ]