from operator import mod
from rest_framework import serializers
from volunteers.models import *
# from backend.heartflow.volunteers.models import *


class volunteerSerializer(serializers.ModelSerializer):
    branch = serializers.SlugRelatedField(slug_field='name', read_only = True)
    class Meta:
        model = Volunteers
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }

class branchSerializer(serializers.ModelSerializer):
    class Meta:
        model = branch
        fields = '__all__'

class pikedUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickedUp
        fields = '__all__'

class discardLostSerializer(serializers.ModelSerializer):
    class Meta:
        model = discardLost
        fields = '__all__'

class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = '__all__'

class deliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = delivery
        fields = '__all__'

class exchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = exchanges
        fields = '__all__'

class volunteerCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = volunteerCoupons
        fields = '__all__'

class sourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = source
        fields = '__all__'

