from rest_framework import serializers
from Parents.models import SoCheckins


class SoCheckinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoCheckins
        fields = '__all__'
