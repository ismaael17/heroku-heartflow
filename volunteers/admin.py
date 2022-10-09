from django.contrib import admin
from .models import Companies, PickedUp, Volunteers, branch, exchanges, discardLost, volunteerCoupons, delivery, source

class VolunteersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email','branch', 'couponAmount', 'status', 'reason', 'registerDate', 'phone')
    list_filter = ('branch',)
    search_fields = ('name', 'surname', 'email', 'branch', 'couponAmount', 'status')

class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('companyName', 'repName', 'repEmail', 'address', 'branch', 'upToDate', 'payment_method', 'volunteer', 'phone')
    list_filter = ('branch',)
    search_fields = ('companyName', 'repName', 'repEmail', 'address', 'branch', 'upToDate', 'payment_method', 'volunteer')

class PickedUpAdmin(admin.ModelAdmin):
    list_display = ('amount', 'source', 'serial_letter', 'range_from', 'range_to', 'date', 'volunteer')
    list_filter = ('volunteer',)
    search_fields = ('amount', 'source', 'serial_letter', 'range_from', 'range_to', 'date', 'volunteer')

class exchangesAdmin(admin.ModelAdmin):
    list_display = ('amount', 'reason', 'from_volunteer', 'to_volunteer', 'date')
    list_filter = ('from_volunteer', 'to_volunteer')
    search_fields = ('amount', 'reason', 'from_volunteer', 'to_volunteer', 'date')

class branchAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class discardedAdmin(admin.ModelAdmin):
    list_display = ('amount', 'reason', 'volunteer', 'date', 'serial_letter', 'range_from', 'range_to', 'flag')
    list_filter = ('volunteer',)
    search_fields = ('amount', 'reason', 'volunteer', 'date', 'flag')

class volunteerCouponsAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'amount', 'serial_letter', 'range_from', 'range_to')
    list_filter = ('volunteer',)
    search_fields = ('volunteer', 'amount', 'serial_letter', 'range_from', 'range_to')

class deliveryAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'amount', 'serial_letter', 'range_from', 'range_to', 'date')
    list_filter = ('volunteer',)
    search_fields = ('volunteer', 'amount', 'serial_letter', 'range_from', 'range_to', 'date')

class sourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch_source')
    search_fields = ('name', 'branch_source')

admin.site.register(Volunteers, VolunteersAdmin)
admin.site.register(Companies, CompaniesAdmin)
admin.site.register(PickedUp, PickedUpAdmin)
admin.site.register(exchanges, exchangesAdmin)
admin.site.register(branch, branchAdmin)
admin.site.register(discardLost, discardedAdmin)
admin.site.register(volunteerCoupons, volunteerCouponsAdmin)
admin.site.register(delivery, deliveryAdmin)
admin.site.register(source, sourceAdmin)

# Register your models here.
