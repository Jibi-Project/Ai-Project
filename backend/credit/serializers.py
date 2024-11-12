from rest_framework import serializers
from .models import Credit

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'
