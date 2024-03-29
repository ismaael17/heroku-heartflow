# Generated by Django 4.1 on 2022-10-09 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('couponAmount', models.IntegerField(default=0)),
                ('status', models.CharField(default='pending_review', max_length=30)),
                ('reason', models.TextField(blank=True, default='')),
                ('registerDate', models.DateField(auto_now_add=True)),
                ('phone', models.CharField(default='', max_length=20)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=255)),
                ('repName', models.CharField(max_length=255)),
                ('repEmail', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('upToDate', models.BooleanField(default=False)),
                ('payment_method', models.CharField(max_length=255)),
                ('policy', models.CharField(default='None', max_length=255)),
                ('phone', models.CharField(default='', max_length=20)),
                ('branch', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='volunteers.branch')),
                ('volunteer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='volunteerCoupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('serial_letter', models.CharField(default='A', max_length=1)),
                ('range_from', models.IntegerField(default=0)),
                ('range_to', models.IntegerField(default=0)),
                ('volunteer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('branch_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_source', to='volunteers.branch')),
            ],
        ),
        migrations.CreateModel(
            name='PickedUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('source', models.CharField(max_length=255, null=True)),
                ('serial_letter', models.CharField(default='A', max_length=1)),
                ('range_from', models.IntegerField(default=0)),
                ('range_to', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('volunteer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='exchanges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('range_from', models.IntegerField(default=0)),
                ('range_to', models.IntegerField(default=0)),
                ('flag', models.BooleanField(default=False)),
                ('serial_letter', models.CharField(default='A', max_length=1)),
                ('date', models.DateTimeField(auto_now=True)),
                ('from_volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_volunteer', to=settings.AUTH_USER_MODEL)),
                ('to_volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_volunteer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='discardLost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('serial_letter', models.CharField(default='A', max_length=1)),
                ('range_from', models.IntegerField(default=0)),
                ('range_to', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('reason', models.TextField()),
                ('flag', models.BooleanField(default=False)),
                ('volunteer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('serial_letter', models.CharField(default='A', max_length=1)),
                ('range_from', models.IntegerField(default=0)),
                ('range_to', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('comments', models.TextField()),
                ('outlet', models.CharField(default='', max_length=255)),
                ('paymentMethod', models.CharField(default='None', max_length=255)),
                ('flag', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('company', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='volunteers.companies')),
                ('volunteer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='volunteers',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='volunteers.branch'),
        ),
        migrations.AddField(
            model_name='volunteers',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
