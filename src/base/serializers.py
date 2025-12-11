from rest_framework import serializers

from src.base.models import RegistryModel


class CallerIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistryModel
        fields = ('operator', 'region', 'territory', 'inn')
