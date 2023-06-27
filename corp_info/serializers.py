from rest_framework import serializers
from .models import Corporation, SmartLogistics, Technology


class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = '__all__'


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'


class SmartLogisticsSerializer(serializers.ModelSerializer):
    technology = TechnologySerializer()

    class Meta:
        model = SmartLogistics
        fields = '__all__'