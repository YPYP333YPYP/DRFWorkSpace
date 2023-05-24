from rest_framework import serializers
from .models import Corporation

class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = '__all__'
