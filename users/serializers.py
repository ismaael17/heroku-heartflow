from rest_framework import serializers
from users.models import *


class transactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineCoupons
        fields = '__all__'
