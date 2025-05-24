from rest_framework import serializers
from Students.models.SoClassUsers import SoClassUserss
from Students.models.SoClasses import SoClasses
from Students.serializers.so_classes_serializer import SoClassesSerializer
from Users.models.souser import SoUser
from Users.serializers.so_user_serializer import SoUserSerializer
class SoClassUsersSerializer(serializers.ModelSerializer):
    soClassName = serializers.SerializerMethodField()
    soUserName = serializers.SerializerMethodField()
    class Meta:
        model = SoClassUserss
        fields = ['id', 'soClassId', 'soUserId','soClassName', 'soUserName']
    def get_soClassName(self, obj):
        try:
            soClassName = SoClasses.objects.filter(id=obj.soClassId).first()
            return SoClassesSerializer(soClassName).data['name']
        except SoClasses.DoesNotExist:
            return None
    def get_soUserName(self, obj):
        try:
            soUserName = SoUser.objects.filter(id=obj.soUserId).first()
            return SoUserSerializer(soUserName).data['name']
        except SoUser.DoesNotExist:
            return None