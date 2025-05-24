from rest_framework import serializers
from Users.models import SoUser
from Users.models import SoRole
import json

class SoUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # username = serializers.CharField(write_only=True)
    name_roles = serializers.SerializerMethodField()

    class Meta:
        model = SoUser
        fields = ['id', 'username', 'password', 'name', 'dob', 'phone', 'email', 'address', 'nationalId', 'avt', 'soRoleIds', 'name_roles']

    def get_name_roles(self, obj):
        role_ids = obj.soRoleIds  # Đây là list các UUID string
        role_names = []

        if isinstance(role_ids, list):
            for role_id in role_ids:
                role = SoRole.objects.filter(id=role_id).first()
                if role:
                    role_names.append(role.name)
                else:
                    role_names.append("Không xác định")
            return ", ".join(role_names)
    
        return "Không có vai trò"
    def create(self, validated_data):
        user = SoUser.objects.create_user(**validated_data)
        return user
