from django.contrib import admin
from .models import *
class OnlineCouponsAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'paid', 'address', 'email', 'name', 'surname', 'dateOfOrder', 'payfastRef', 'branch', 'status')
    list_filter = ('name', 'email')
    search_fields = ('id', 'amount', 'paid', 'address', 'email', 'name', 'surname', 'dateOfOrder', 'payfastRef', 'branch', 'status')

class CouponShopAdmin(admin.ModelAdmin):
    list_display = ('companyName', 'email', 'amount', 'shopCoupons')
    list_filter = ('companyName',)
    search_fields = ('companyName', 'email', 'amount', 'shopCoupons')

class ShopCouponsAdmin(admin.ModelAdmin):
    list_display = ('amount', 'snapscanCode', 'date')
    list_filter = ('date',)
    search_fields = ('amount', 'snapscanCode', 'date')

class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', 'amount', 'name', 'surname', 'branch')
    list_filter = ('branch',)
    search_fields = ('email', 'date', 'amount', 'name', 'surname', 'branch')


admin.site.register(OnlineCoupons, OnlineCouponsAdmin)
admin.site.register(CouponShop, CouponShopAdmin)
admin.site.register(ShopCoupons, ShopCouponsAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)


# Register your models here.
