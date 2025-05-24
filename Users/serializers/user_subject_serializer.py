from rest_framework import serializers
from ..models.user_subject import UserSubject

class UserSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubject
        fields = ['id', 'user_id', 'subject_id', 'created_at']
