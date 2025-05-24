from rest_framework import serializers
from ..models.teacher_role import TeacherRole

class TeacherRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherRole
        fields = ['id', 'user_id', 'role_type', 'created_at']
