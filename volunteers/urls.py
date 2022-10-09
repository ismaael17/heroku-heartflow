from django.urls import re_path, path

# from volunteers import views
from volunteers import views
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^volunteers$', views.volunteersCRUD),
    re_path(r'^branch$', views.branchCRUD),
    path('login', obtain_auth_token, name='login'),
    path('reset-password/<token>', views.resetPassword, name = 'reset-password/token'),
    re_path(r'^get-pending-volunteers', views.pendingVolunteer.as_view(), name = 'pending-volunteers'),
    re_path(r'^pending-volunteers/(?P<status>\w+)/$', views.pendingVolunteer.as_view(), name = 'pending-volunteers'),
    path('user-type', views.userType.as_view(), name = 'user-type'),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='./registration/password_reset_form.html'), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('coupons/<status>', views.coupons.as_view(), name = 'coupons'),
    path('coupon/id=<id>', views.coupons.as_view(), name = 'coupons'),
    path('updatecoupons/<id>', views.coupons.as_view(), name = 'coupons'),
    path('picked-up', views.pickedUp.as_view(), name = 'pickedup'),
    path('discard-lost', views.discardLost.as_view(), name = 'discardLost'),
    path('get-info', views.volunteerInfo.as_view(), name = 'get-info'),
    path('get-info/<id>', views.volunteerInfo.as_view(), name = 'get-info'),
    path('register-company', views.registerCompany.as_view(), name = 'register-company'),
    path('register-company/<id>', views.registerCompany.as_view(), name = 'register-company/<id>'),
    path('discard-coupons', views.discardLost.as_view(), name = 'discard-coupons'),
    path('deliver', views.deliver.as_view(), name = 'deliver'),
    path('exchange-coupons', views.exchange.as_view(), name = 'exchange-coupons'),
    path('source',views.sources.as_view(), name = 'source'),
    path('get-volunteers-exchange', views.volunteerExchangeInfo.as_view(), name = 'get-volunteers-exchange'),
]  
