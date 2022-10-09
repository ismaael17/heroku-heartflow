# Generated by Django 4.1 on 2022-10-09 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('volunteers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteers.branch'),
        ),
        migrations.AddField(
            model_name='couponshop',
            name='shopCoupons',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.shopcoupons'),
        ),
    ]
