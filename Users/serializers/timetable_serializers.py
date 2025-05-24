# # serializers.py
# from rest_framework import serializers
# from Users.models.Timetables import Timetable
# from Users.models.souser import SoUser
# from Users.serializers.subject_serializer import SubjectSerializer
# from Users.serializers.so_user_serializer import SoUserSerializer
# from Users.models.subject import Subject

# class TimetableSerializer(serializers.ModelSerializer):
#     subject = SubjectSerializer(read_only = True)
#     subject_name = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(),source='subject.name',write_only = True)
#     user = serializers.StringRelatedField(source='soUser.name')  # Lấy tên giáo viên
#     classroom = serializers.StringRelatedField(source='class_id.name')  # Lấy tên phòng học

#     class Meta:
#         model = Timetable
#         fields = ['id', 'subject','subject_name', 'user', 'classroom', 'date', 'start_time', 'end_time']


# serializers.py
from rest_framework import serializers
from Users.models.Timetables import Timetable
from Users.models.subject import Subject
from Users.models.souser import SoUser
from Students.models.SoClasses import SoClasses
from Users.serializers.subject_serializer import SubjectSerializer
from Users.serializers.so_user_serializer import SoUserSerializer
from Students.serializers.so_classes_serializer import SoClassesSerializer

class TimetableSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(write_only=True)
    teacher_id = serializers.CharField(write_only=True)  
    class_id = serializers.CharField(write_only=True)    

    subject_detail = serializers.SerializerMethodField(read_only=True)
    teacher_detail = serializers.SerializerMethodField(read_only=True)
    class_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Timetable
        fields = [
            'id',
            'subject_name',
            'teacher_id',
            'class_id',
            'subject_detail',
            'teacher_detail',
            'class_detail',
            'date',
            'start_time',
            'end_time',
        ]

    def get_subject_detail(self, obj):
        try:
            subject = Subject.objects.get(id=obj.subject_id)
            return SubjectSerializer(subject).data
        except Subject.DoesNotExist:
            return None

    def get_teacher_detail(self, obj):
        try:
            teacher = SoUser.objects.get(id=obj.teacher_id)
            serialized  = SoUserSerializer(teacher).data
            serialized.pop('soRoleIds', None)  
            serialized.pop('name_roles', None)  
            serialized.pop('username', None)  
            return serialized
        except SoUser.DoesNotExist:
            return None

    def get_class_detail(self, obj):
        try:
            class_obj = SoClasses.objects.get(id=obj.class_id)
            return SoClassesSerializer(class_obj).data
        except SoClasses.DoesNotExist:
            return None

    def create(self, validated_data):
        subject_id = validated_data.pop("subject_name")
        return Timetable.objects.create(subject_id=subject_id, **validated_data)
