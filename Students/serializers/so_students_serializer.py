from rest_framework import serializers
from Students.models.SoStudents import SoStudent

class SoStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoStudent
        fields = ['id', 'name', 'dob', 'gender', 'phone', 'email', 'address', 'nationalId', 'avt', 'soClassId']
