from rest_framework import serializers
import api.models as models
import json


class GrowlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Growler
        fields = '__all__'


class RefillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Refill
        fields = '__all__'
