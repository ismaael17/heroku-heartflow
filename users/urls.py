from django.urls import re_path, path
from users import views

urlpatterns = [
    re_path(r'^signature$', views.signature),
    re_path(r'^notificationPage$', views.notificationPage),
    re_path(r'^insertTransaction$', views.insertTransaction),
    re_path(r'^cancelTransaction$', views.cancelTransaction),
]
