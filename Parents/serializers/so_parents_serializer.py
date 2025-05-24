from rest_framework import serializers
from Parents.models import SoParents

class SoParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoParents
        fields = '__all__'
