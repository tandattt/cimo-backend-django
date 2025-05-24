# Parents/serializers/so_student_off_serializer.py
from rest_framework import serializers
from Students.models.SoStudentOff import SoStudentOff
from Students.serializers.so_students_serializer import SoStudentsSerializer
from Parents.serializers.so_parents_serializer import SoParentsSerializer
from Students.models.SoStudents import SoStudent
from Parents.models import SoParents
from Students.models.SoClasses import SoClasses
from Students.serializers.so_classes_serializer import SoClassesSerializer
from Users.models import SoUser
from Users.serializers.so_user_serializer import SoUserSerializer

class SoStudentOffSerializer(serializers.ModelSerializer):
    # student = serializers.SerializerMethodField()
    # parent = serializers.SerializerMethodField()
    soStudentName = serializers.SerializerMethodField()
    soParentName = serializers.SerializerMethodField()
    relation = serializers.SerializerMethodField()
    class Meta:
        model = SoStudentOff
        fields = [
            'id', 'soStudentId','soStudentName',
            'soParentId', 'soParentName',
            'relation',
            'leaveStartDate', 'leaveEndDate',
            'reason', 'note', 'leaveStatus',
            'createdDate', 'updatedDate', 'createdBy', 'updatedBy', 'soClassId', 'soUserId',
        ]
        extra_kwargs = {
            'note': {'allow_null': True, 'required': False},
            'soUserId': {'allow_null': True, 'required': False},
            'updatedBy': {'allow_null': True, 'required': False},
            'createdBy': {'allow_null': True, 'required': False},
            'updatedDate': {'allow_null': True, 'required': False},
        }
    def get_relation(self, obj):
        try:
            parent = SoParents.objects.get(id=obj.soParentId)
            return parent.relation  # hoặc .name tùy vào model của bạn
        except SoParents.DoesNotExist:
            return None
    def get_soStudentName(self, obj):
        try:
            student = SoStudent.objects.get(id=obj.soStudentId)
            return student.name  # hoặc .name tùy vào model của bạn
        except SoStudent.DoesNotExist:
            return None

    def get_soParentName(self, obj):
        try:
            parent = SoParents.objects.get(id=obj.soParentId)
            return parent.name  # hoặc .name
        except SoParents.DoesNotExist:
            return None
    def get_student(self, obj):
        try:
            # from Students.models import SoStudent
            student = SoStudent.objects.get(id=obj.soStudentId)
            # from Students.serializers.so_students_serializer import SoStudentsSerializer
            return SoStudentsSerializer(student).data
        except SoStudent.DoesNotExist:
            return None
    def get_approved_by(self, obj):
        try:
            # from Users.models import SoUser
            approved_by = SoUser.objects.get(id=obj.soUserId)
            # from Users.serializers.so_user_serializer import SoUserSerializer
            return SoUserSerializer(approved_by).data
        except SoUser.DoesNotExist:
            return None
    def get_parent(self, obj):
        try:
            # from Parents.models import SoParents
            parent = SoParents.objects.get(id=obj.soParentId)
            # from Parents.serializers.so_parents_serializer import SoParentsSerializer
            return SoParentsSerializer(parent).data
        except SoParents.DoesNotExist:
            return None
    def get_class(self, obj):
        try:
            # from Students.models import SoClasses
            class_instance = SoClasses.objects.get(id=obj.soClassId)
            # from Students.serializers.so_classes_serializer import SoClassesSerializer
            return SoClassesSerializer(class_instance).data
        except SoClasses.DoesNotExist:
            return None