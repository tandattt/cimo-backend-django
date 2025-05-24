from django.shortcuts import render
from rest_framework import viewsets
from .models import SoCheckins
from .serializers import SoCheckinsSerializer
from Users.models import SoUser,SoRole
from Users.serializers import SoUserSerializer
from Students.models.SoStudents import SoStudent
from Students.models.SoStudentOff import SoStudentOff
from Students.serializers.so_student_off_serializer import SoStudentOffSerializer
from Students.models.SoClasses import SoClasses
from Students.models.SoClassUsers import SoClassUserss
from Students.serializers.so_class_users_serializer import SoClassUsersSerializer
from Students.serializers.so_classes_serializer import SoClassesSerializer
from Students.serializers.so_students_serializer import SoStudentsSerializer
from Parents.models import SoStudentParents,SoParents
from Parents.serializers import SoStudentParentsSerializer,SoParentsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta,datetime
import uuid
import json
from Auth.views import veriry_token


class SoCheckinsViewSet(viewsets.ModelViewSet):
    queryset = SoCheckins.objects.all()
    serializer_class = SoCheckinsSerializer

    def get_queryset(self):
        # Chỉ lấy những bản ghi chưa bị đánh dấu xoá (nếu bạn sử dụng BaseModel)
        return SoCheckins.objects.filter(isDeleted=False)

    def perform_destroy(self, instance):
        # Thay vì xóa hẳn, ta đánh dấu là deleted
        instance.isDeleted = True
        instance.save()

class bot_process_leave_request(APIView):
    # permission_classes=[AllowAny]
    def post(self, request):
        data = request.data
        student_name = data.get('student_name')
        # leave_date = data.get('leave_date')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        reason = data.get('reason')
        sender_id = data.get('sender_id')

        # Kiểm tra phụ huynh tồn tại không:
        try:
            # print(sender_id)
            parent_instance = SoParents.objects.filter(id=sender_id).first()
            # print(parent_instance)
        except SoParents.DoesNotExist:
            return Response({"error": "Phụ huynh không tồn tại."}, status=404)
        student_parents = SoStudentParents.objects.filter(soParentid=sender_id)

        if not student_parents.exists():
            return Response({"error": "Không tìm thấy học sinh liên kết với phụ huynh này."}, status=404)
        # print(student_name)
        for i in student_name:
            # print(i)

            student_main = None
            # Tìm đúng học sinh dựa trên tên
            for student_parent in student_parents:
                student = SoStudent.objects.filter(id=student_parent.soStudentid, name=i).first()
                if student:
                    student_main = student
                    break

            # Không tìm thấy học sinh nào đúng tên
            if student_main is None:
                return Response({"error": f"Không tìm thấy học sinh có tên '{i}' liên kết với phụ huynh này."}, status=404)

            # Chuyển leave_date đúng format
            # leave_date = datetime.strptime(leave_date, "%d/%m").replace(year=2025).strftime("%Y-%m-%d")
            # if leave_date and '/' in leave_date:
            #     # Định dạng là 'ngày/tháng'
            #     leave_date = datetime.strptime(leave_date, "%d/%m").replace(year=2025).strftime("%Y-%m-%d")
            # elif leave_date and '-' in leave_date:
            #     # Định dạng là 'YYYY-MM-DD'
            #     leave_date = datetime.strptime(leave_date, "%Y-%m-%d").strftime("%Y-%m-%d")

            
            # print(student_main.id)
            # print(parent_instance.id)
            SoStudentOff.objects.create(
                id=uuid.uuid4(),
                soStudentId=student_main.id,  
                soParentId=parent_instance.id,
                leaveStartDate=start_date,
                leaveEndDate=end_date,
                reason=reason,
                leaveStatus="pending",
                soClassId =student_main.soClassId,
            )

        return Response({
            "message": f"Đã ghi nhận yêu cầu nghỉ học cho '{student_name}' từ ngày {start_date} đến ngày {end_date} vui lòng đợi giới viên duyệt nhé.",
            # "request_id": leave_request.id
        }, status=200)



class SoPerentsAPI(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        result = veriry_token(auth_header)
        payload = result.get('payload')
        print(payload.get("parent"))
        SoParent = SoParents.objects.filter(id=payload.get("parent")).first()
        # print(SoParent)
        SoParentSerializer = SoParentsSerializer(SoParent)
        
        if not SoParent:
            return Response({'error': 'Phụ huynh không tồn tại'}, status=404)
        parent_info =SoParentSerializer.data
        student_parents = SoStudentParents.objects.filter(soParentid=SoParent.id)
        if not student_parents.exists():
            return Response({'error': 'Phụ huynh không có học sinh nào'}, status=404)
        list_student = []
        for student_parent in student_parents:
            student = SoStudent.objects.filter(id=student_parent.soStudentid).first()
            if student:
                student_serializer = SoStudentsSerializer(student)
                student_data=student_serializer.data
                class_info = SoClasses.objects.filter(id=student.soClassId).first()
                if class_info:
                    class_serializer = SoClassesSerializer(class_info)
                    teacher_info = {
                        'id': class_serializer.data['id'],
                        'name': class_serializer.data['name']
                    }
                    student_data.pop('soClassId', None)
                    # print(student.soClassId)
                    class_users = SoClassUserss.objects.filter(soClassId=student.soClassId)
                    # print(class_users)
                    if class_users.exists():
                        for class_user in class_users:
                            teacher = SoUser.objects.filter(id=class_user.soUserId).first()
                            if teacher:
                                teacher_serializer = SoUserSerializer(teacher)
                                roles =[]
                                role_ids = json.loads(teacher_serializer.data.get('soRoleIds'))
                                # print(role_ids)
                                for role_id in role_ids:
                                    role = SoRole.objects.filter(id=role_id).first()
                                    # print(role_id)
                                    if role:
                                        roles.append({
                                            'id':role.id,
                                            'name':role.name
                                        }
                                        )
                                    # roles.append(role)
                                teacher_info['soUsers'] = {
                                    'id': teacher_serializer.data['id'],
                                    'name': teacher_serializer.data['name'],
                                    'role': roles,
                                }
                                
                            else:
                                student_data['soUsers'] = None
                    student_data['soClass'] = teacher_info            
                    list_student.append(student_data) 
                    
                else:
                    return Response({'error': 'Không tìm thấy lớp học'}, status=404)
                # list_student['soClassId'] = student.soClassId
            else:
                return Response({'error': 'Không tìm thấy học sinh'}, status=404)
        parent_info['students'] = list_student
        return Response(parent_info, status=200)
    
class process_leave_request(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        result = veriry_token(auth_header)
        if result['valid'] == False:
            return Response(result['error'],status=401)
        payload = result.get('payload')
        data = request.data.copy()
        # data['student_id'] = data.get('soStudentId')
        data['soParentId'] = payload.get("parent")
        # data['class_id'] = data.get('soClassId')
        # print(data)
        serializer = SoStudentOffSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"oke nha bờ gô"}, status=201)
        else:
            return Response(serializer.errors, status=400)
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        result = veriry_token(auth_header)
        if result['valid'] == False:
            return Response(result['error'],status=401)
        payload = result.get('payload')
        student_offs = SoStudentOff.objects.filter(soParentId=payload.get("parent"))
        serializer = SoStudentOffSerializer(student_offs, many=True)    
        result = []
        for i in range(len(serializer.data)):

            result.append({
                'id': serializer.data[i]['id'],
                'soStudentId': serializer.data[i]['soStudentId'],
                'soParentId': serializer.data[i]['soParentId'],
                'leaveStartDate': serializer.data[i]['leaveStartDate'],
                'leaveEndDate': serializer.data[i]['leaveEndDate'],
                'reason': serializer.data[i]['reason'],
                'leaveStatus': serializer.data[i]['leaveStatus'],
                'createdDate': serializer.data[i]['createdDate'],
                'soUserId': serializer.data[i]['soUserId'],
            })
        return Response(result, status=200)
