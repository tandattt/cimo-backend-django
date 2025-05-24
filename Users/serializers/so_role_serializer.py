from rest_framework import serializers
from Users.models import SoRole

class SoRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoRole
        fields = '__all__'
