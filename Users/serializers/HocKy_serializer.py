
from rest_framework import serializers
from ..models.HocKy import HocKy

class HocKySerializer(serializers.ModelSerializer):
    class Meta:
        model = HocKy
        fields = ['id', 'ten_hoc_ky', 'nam_hoc', 'start_date', 'end_date']
