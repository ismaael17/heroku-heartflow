import uuid

from django.db import models
#from backend.heartflow.volunteers.models import branch
from volunteers.models import branch


# Create your models here.
# class Directors(models.Model):
#     name = models.CharField(max_length=255, null=False)
#     surname = models.CharField(max_length=255, null=False)
#     email = models.CharField(max_length=255, null=False)
#     password = models.CharField(max_length=255, null=False)


class OnlineCoupons(models.Model):
    amount = models.IntegerField(null=False)
    paid = models.IntegerField(null=False, default=0)
    address = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    surname = models.CharField(max_length=255, null=False)
    dateOfOrder = models.DateTimeField(auto_now=True, null=False)
    payfastRef = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    branch = models.CharField(max_length=100, null=False)
    status = models.CharField(max_length=100, null=False)


class CouponShop(models.Model):
    companyName = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    amount = models.IntegerField(null=False)
    shopCoupons = models.ForeignKey("ShopCoupons", on_delete=models.CASCADE)


class ShopCoupons(models.Model):
    amount = models.IntegerField(null=False)
    snapscanCode = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now=True, null=False)  # Possible auto_now = True?

class Subscriptions(models.Model):
    email = models.CharField(max_length=255, null=False)
    date = models.DateTimeField(auto_now=True, null=False)  # Possible auto_now = True?
    amount = models.IntegerField(null=False)
    name = models.CharField(max_length=255, null=False)
    surname = models.CharField(max_length=255, null=False)
    branch = models.ForeignKey(branch, on_delete=models.CASCADE)



# Create your models here.
