
from rest_framework import serializers
from ..models.Diem import Diem

class DiemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diem
        fields = [
            'id', 'soStudentId', 'subject_id', 'hoc_ky_id',
            'diem_15p', 'diem_mieng', 'diem_1tiet', 'diem_hk', 'diem_tb','soClassesId'
        ]
