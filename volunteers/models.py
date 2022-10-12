# Create your models here.
from pyexpat import model
from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
class Volunteers(AbstractUser):
    username = None
    groups = None
    email = models.EmailField(_('email address'), unique=True)
    branch = models.ForeignKey("branch", on_delete=models.CASCADE, null=True)
    couponAmount = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default="pending_review")
    reason = models.TextField(default="", blank=True)
    registerDate = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=20, default="", null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class discardLost(models.Model):
    amount = models.IntegerField(null=False)
    serial_letter = models.CharField(max_length=1, null=False, default="A")
    range_from = models.IntegerField(default=0)
    range_to = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True, null=False)
    reason = models.TextField(null=False)
    volunteer = models.ForeignKey("Volunteers", on_delete=models.CASCADE, null=True)
    flag = models.BooleanField(default=False)


class PickedUp(models.Model):
    amount = models.IntegerField(null=False)
    source = models.CharField(max_length=255, null=True)
    serial_letter = models.CharField(max_length=1, null=False, default="A")
    range_from = models.IntegerField(default=0)
    range_to = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True, null=False)
    volunteer = models.ForeignKey("Volunteers", on_delete=models.CASCADE, null=True)


class Companies(models.Model):
    companyName = models.CharField(max_length=255, null=False)
    repName = models.CharField(max_length=255, null=False)
    repEmail = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    branch = models.ForeignKey("branch", on_delete=models.CASCADE, null=False)
    upToDate = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=255, null=False)
    policy = models.CharField(max_length=255, null=False)
    volunteer = models.ForeignKey("Volunteers", on_delete=models.CASCADE, null=True)
    policy = models.CharField(max_length=255, null=False, default="None")
    phone = models.CharField(max_length=20, default="", null=False)
    active = models.BooleanField(default=True)

class exchanges(models.Model):
    amount = models.IntegerField(null=False)
    reason = models.TextField
    from_volunteer = models.ForeignKey("Volunteers", on_delete=models.CASCADE, related_name="from_volunteer",
                                       null=False)
    to_volunteer = models.ForeignKey("Volunteers", on_delete=models.CASCADE, related_name="to_volunteer", null=False)
    range_from = models.IntegerField(null=False, default=0)
    range_to = models.IntegerField(null=False, default=0)
    flag = models.BooleanField(default=False)
    serial_letter = models.CharField(max_length=1, null=False, default='A')
    date = models.DateTimeField(auto_now=True, null=False)


class branch(models.Model):
    name = models.CharField(max_length=255, null=False)


class source(models.Model):
    name = models.CharField(max_length=255, null=False)
    branch_source = models.ForeignKey("branch", on_delete=models.CASCADE, related_name="branch_source", null=False)


class delivery(models.Model):
    amount = models.IntegerField(null=False)
    serial_letter = models.CharField(max_length=1, null=False, default="A")
    range_from = models.IntegerField(default=0)
    range_to = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True, null=False)
    comments = models.TextField(null=False)
    volunteer = models.ForeignKey("Volunteers", on_delete=models.CASCADE, null=True)
    paymentMethod = models.CharField(max_length=255, null=False, default="None")
    flag = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    company = models.ForeignKey("Companies", on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255, null=False, default="None")


class volunteerCoupons(models.Model):
    amount = models.IntegerField(null=False)
    serial_letter = models.CharField(max_length=1, null=False, default="A")
    range_from = models.IntegerField(default=0)
    range_to = models.IntegerField(default=0)
    volunteer = models.ForeignKey("Volunteers", on_delete=models.CASCADE, null=True)
