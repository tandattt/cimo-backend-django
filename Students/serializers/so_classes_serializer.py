from rest_framework import serializers
from Students.models.SoClasses import SoClasses

class SoClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoClasses
        fields = ['id', 'name']
