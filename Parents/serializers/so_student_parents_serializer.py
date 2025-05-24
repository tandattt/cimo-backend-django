from rest_framework import serializers
from Parents.models import SoStudentParents

class SoStudentParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoStudentParents
        fields = ['id', 'soStudentid', 'soParentid']
