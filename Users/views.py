from rest_framework.views import APIView
from rest_framework.response import Response
from .models.Timetables import Timetable
from .models.subject import Subject
from .models.souser import SoUser
from .serializers.so_user_serializer import SoUserSerializer
from Students.models.SoClasses import SoClasses
from Students.models.SoClassUsers import SoClassUserss
from Students.models.SoStudentOff import SoStudentOff
from Students.serializers.so_student_off_serializer import SoStudentOffSerializer
from Students.serializers.so_class_users_serializer import SoClassUsersSerializer
from Students.models.SoStudents import SoStudent
from Students.serializers.so_students_serializer import SoStudentsSerializer
from Parents.models.SoParents import SoParents
from Parents.serializers.so_parents_serializer import SoParentsSerializer
from Students.serializers.so_classes_serializer import SoClassesSerializer
from .serializers.subject_serializer import SubjectSerializer
from .serializers.timetable_serializers import TimetableSerializer
from Parents.models.SoStudentParents import SoStudentParents
from datetime import datetime, timedelta, date
from django.utils import timezone
from Parents.serializers.so_checkins_serializer import SoCheckinsSerializer
from Parents.models.SoCheckins import SoCheckins
import uuid
from Auth.views import veriry_token
from Users.models.sorole import SoRole
from Users.serializers.so_role_serializer import SoRoleSerializer
import json
from .models.user_subject import UserSubject
from .models.teacher_role import TeacherRole
from .serializers.user_subject_serializer import UserSubjectSerializer
from .serializers.teacher_role_serializer import TeacherRoleSerializer
from .models.subject import Subject
from .models.Diem import Diem
from .serializers.subject_serializer import SubjectSerializer
from .serializers.Diem_serializer import DiemSerializer
from .models.HocKy import HocKy
from .serializers.HocKy_serializer import HocKySerializer
from collections import defaultdict
from utils.decorator import logger

class CheckinAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        student = request.data.get('soStudentId')
        Class = request.data.get('soClassId')
        teacher = request.data.get('createdBy')
        note = request.data.get('note')
        checkType = request.data.get('checkType')
        
        checkDate = datetime.now()
        
        SoCheckins.objects.create(id = uuid.uuid4(),soStudentId=student, soClassesId=Class, createdBy=teacher, note=note, checkType=checkType, checkDate=checkDate)
        return Response({"message":"success"})
    

class TimetableAPIView(APIView):
    @logger("log","get_timetable")
    def get(self, request, *args, **kwargs):
        class_id = request.query_params.get('class_id')
        start_date_str = request.query_params.get('date')  # yyyy-mm-dd

        if not class_id:
            return Response({"error": "Vui lòng cung cấp ID lớp học."}, status=400)
        if not start_date_str:
            return Response({"error": "Vui lòng cung cấp ngày bắt đầu (YYYY-MM-DD)."}, status=400)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Định dạng ngày không hợp lệ. Đúng định dạng: YYYY-MM-DD"}, status=400)

        end_date = start_date + timedelta(days=6)

        timetables = Timetable.objects.filter(
            class_id=class_id,
            date__range=(start_date, end_date)
        ).order_by('date')

        if not timetables.exists():
            return Response({"message": "Không có lịch học nào trong 7 ngày tới."}, status=404)
        
        serialized = TimetableSerializer(timetables, many=True).data

        grouped_by_date = defaultdict(list)
        for lesson in serialized:
            date = lesson['date']
            lesson.pop('date', None)
            grouped_by_date[date].append(lesson)

        # Tạo cấu trúc mới theo từng ngày
        result = []
        for date, lessons in grouped_by_date.items():
            result.append({
                "date": date,
                "lessons": lessons
            })

        return Response(result, status=200)
    @logger("log","post_timetable")
    def post(self, request, *args, **kwargs):
        data = request.data
        Subject_name  = data.get('subject_name')
        teacher_id = data.get('teacher_id')
        subject = Subject.objects.filter(name = Subject_name).first()
        user = SoUser.objects.filter(id = teacher_id).first()
        # print(user)
        if not subject:
            return Response({"error": "Không tìm thấy môn học."}, status=400)
        subject_id = subject.id
        # print(subject_id)
        class_id = data.get('class_id')
        if not class_id:
            return Response({"error": "Vui lòng cung cấp ID lớp học."}, status=400)
        date = data.get('date')
        if not date:
            return Response({"error": "Vui lòng cung cấp ngày."}, status=400)
        start_time = data.get('start_time')
        if not start_time:
            return Response({"error": "Vui lòng cung cấp thời gian bắt đầu."}, status=400)
        # Chuyển chuỗi sang datetime trước khi cộng
        start_time_dt = datetime.strptime(start_time, "%H:%M:%S")
        end_time_dt = start_time_dt + timedelta(minutes=45)

        # Chuyển lại về chuỗi để lưu
        start_time_str = start_time_dt.strftime("%H:%M:%S")
        end_time = end_time_dt.strftime("%H:%M:%S")
        timetable ={
                        "subject_name": subject_id,
                        "class_id": class_id,   
                        "teacher_id": user.id,
                        "date": date,
                        "start_time": start_time_str,
                        "end_time": end_time,
                    }
        timetable_serializer = TimetableSerializer(data=timetable)
        timetable_serializer.is_valid(raise_exception=True)
        timetable_serializer.save()
        return Response(timetable_serializer.data, status=201)
class Bot_TimetableAPIView(APIView):
    def post(self, request, *args, **kwargs):
        student_names = request.data.get('student_name')
        sender_id = request.data.get('sender_id')
        # print(student_names)
        if not student_names:
            return Response({"error": "Vui lòng cung cấp tên học sinh."}, status=400)
        
        # class_id = request.data.get('class')
        student_parents = SoStudentParents.objects.filter(soParentid=sender_id)
        # print(student_parents)
        if not student_parents.exists():
            return Response({"error": "Không tìm thấy học sinh liên kết với phụ huynh này."}, status=400)
        # print(student_name)
        lists = []
        for student_name in student_names:
            student_main = None
            for student_parent in student_parents:
                # print(student_parent.soStudentid)
                # print(student_name)
                student = SoStudent.objects.filter(id=student_parent.soStudentid, name=student_name).first()
                if student:
                    student_main = student
                    break
            # print(student_main.soClassId)
            timeTables = Timetable.objects.filter(class_id = student_main.soClassId) 
            if not timeTables.exists():
                return Response({"message":'không có lịch học'},status=400)
            
            for timeTable in timeTables:
                timeTableSerializer = TimetableSerializer(timeTable)
                # print(i.subject_id)
                name_subject = Subject.objects.filter(id=timeTable.subject_id).first()
                name_class = SoClasses.objects.filter(id = timeTable.class_id).first()
                name_teacher = SoUser.objects.filter(id= timeTable.teacher_id).first()
                if not name_subject:
                    return Response({"error": "Không có môn học."}, status=400)

                if not name_class:
                    return Response({"error": "Không có lớp học."}, status=400)
                if not name_teacher:
                    return Response({"error": "Không có giáo viên."}, status=400)
                name_subject_serializer = SubjectSerializer(name_subject)
                name_class_serializer = SoClassesSerializer(name_class)
                name_teacher_serializer = SoUserSerializer(name_teacher)
                # print(name_subject_serializer.data['name'])
                time = timeTableSerializer.data
                time['name_subject'] =name_subject_serializer.data['name']
                time['description'] = name_subject_serializer.data['description']
                time['name_class'] = name_class_serializer.data['name']
                time['name_teacher'] = name_teacher_serializer.data['name']
                lists.append(time)
        return Response(lists)
    
class Get_List_Class(APIView):
    def get(self, request):
        teacher_id = request.query_params.get('teacher_id')
        if not teacher_id:
            return Response({"error": "Vui lòng cung cấp ID giáo viên."}, status=400)
        so_class = SoClassUserss.objects.filter(soUserId=teacher_id)
        classes_serializer = SoClassUsersSerializer(so_class, many=True)
        return Response(classes_serializer.data, status=200)
    
class Get_Detail_Class(APIView):
    def get_number_of_students(self, class_id):
        number_of_students = SoStudent.objects.filter(soClassId=class_id).count()
        return number_of_students
    def get_info_student(self, class_id):
        students = []
        soStudent = SoStudent.objects.filter(soClassId=class_id)
        for student in soStudent:
            student_serializer = SoStudentsSerializer(student)
            soStudentParents = SoStudentParents.objects.filter(soStudentid=student.id)
            parent = []
            for soStudentParent in soStudentParents:
                soparents = SoParents.objects.filter(id=soStudentParent.soParentid).first()
                soparents_serializer = SoParentsSerializer(soparents)
                parent.append({
                    'soParentId': soparents_serializer.data['id'],
                    'soParentName': soparents_serializer.data['name'],
                    'soParentPhone': soparents_serializer.data['phone'],
                    'soParentEmail': soparents_serializer.data['email'],
                    'relation' : soparents_serializer.data['relation']
                })
            students.append({
                'soStudentId': student_serializer.data['id'],
                'soStudentName': student_serializer.data['name'],
                'avt_student': student_serializer.data['avt'],
                'dob_student': student_serializer.data['dob'],
                'gender_student': student_serializer.data['gender'],
                'parents': parent,
            })
        return students
    def get_total_without_permission(self, class_id):
        today = datetime.today().date()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        
        checkins_off = SoCheckins.objects.filter(
            soClassesId=class_id,
            checkType='off',
            checkDate__range=(start, end)
        )
        checkins_serializer = SoCheckinsSerializer(checkins_off, many=True)
        off_student_ids = [item['soStudentId'] for item in checkins_serializer.data]
        # print(off_student_ids)
        final_without_permission = []

        for student_id in off_student_ids:
            has_valid_leave = False

            leave_forms = SoStudentOff.objects.filter(soStudentId=student_id,soClassId=class_id)
            
            for leave in leave_forms:
                try:
                    if leave.leaveStartDate <= today <= leave.leaveEndDate and leave.leaveStatus == 'approved':
                        # print(leave.leaveStartDate, leave.leaveEndDate, today)
                        has_valid_leave = True
                        break
                except:
                    continue

            if not has_valid_leave:
                final_without_permission.append(student_id)
        # print(final_without_permission)
        return final_without_permission
    def get_student_attendance_count(self,class_id):
        today = timezone.now().date()
        # today = '2025-04-15'
        total_with_permission  = SoStudentOff.objects.filter(soClassId=class_id, leaveStartDate__lte = today, leaveEndDate__gte = today, leaveStatus = 'approved')
        # print(total_with_permission)
        total_without_permission = SoStudentOff.objects.filter(soClassId=class_id, leaveStartDate__lte = today, leaveEndDate__gte = today, leaveStatus__in=['rejected', 'pending']).count()
        
        
        # for i in student_checkin:
        student_checkout = SoCheckins.objects.filter(soClassesId=class_id,checkType = 'out',updatedDate__date = today)
        checkout_serializer = SoCheckinsSerializer(student_checkout, many=True)
        # print(checkin_serializer.data)
        checkout_studentId = [item['soStudentId'] for item in checkout_serializer.data]
        present_count = SoCheckins.objects.filter(soClassesId=class_id, checkType = 'in', updatedDate__date = today).exclude(soStudentId__in =checkout_studentId).count()
        # present_count.append(student_checkout)
        # present_count  = student_checkin
        # print(len(present_count))
        return total_with_permission, total_without_permission, present_count
    def get(self, request):
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response({"error": "Vui lòng cung cấp ID lớp học."}, status=400)
        so_class = SoClassUserss.objects.filter(soClassId=class_id)
        classes_serializer = SoClassUsersSerializer(so_class, many=True)
        number_of_students = self.get_number_of_students(class_id)
        total_with_permission,_,present_count = self.get_student_attendance_count(class_id)
        total_without_permission = self.get_total_without_permission(class_id)
        user = []
        for class_ in classes_serializer.data:
            user.append({
                'soUserId' : class_['soUserId'],
                'soUserName' : class_['soUserName'],
                })
        student = self.get_info_student(class_id)
        response_data = ({
                'user': user,
                'number_of_students': number_of_students,
                'total_with_permission': len(total_with_permission),
                'total_without_permission': len(total_without_permission),
                'present_count': present_count,
                'students': student,
            })   
        return Response(response_data, status=200)

class StudentOffAPI(APIView):
    def patch(self, request):
        leave_id = request.query_params.get('leaveId')
        if not leave_id:
            return Response({'error': 'Thiếu leaveId trong query params'}, status=400)

        try:
            student_off = SoStudentOff.objects.get(id=leave_id)
        except SoStudentOff.DoesNotExist:
            return Response({'error': 'Không tìm thấy đơn nghỉ học'}, status=404)
        serializer = SoStudentOffSerializer(student_off, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
        
        
class get_checkin_class(APIView):
    def get(self, request):
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response({"error": "Vui lòng cung cấp ID lớp học."}, status=400)
        today = datetime.today().date()
        start = datetime.combine(today, datetime.min.time())  # 00:00:00
        end = datetime.combine(today, datetime.max.time())    # 23:59:59.999999

        # print(today)
        checkin = SoCheckins.objects.filter(soClassesId=class_id, checkDate__range=(start, end))
        checkin_serializer = SoCheckinsSerializer(checkin, many=True)
        # print(checkin_serializer.data)
        checkin_studenId = [item['soStudentId'] for item in checkin_serializer.data]

        # print(checkin_studenId)
        list_student_checkin = SoStudent.objects.filter(soClassId=class_id).exclude(id__in=checkin_studenId)
        serializer_student = SoStudentsSerializer(list_student_checkin, many=True)
        list_student_checkin = []
        for student in serializer_student.data:
            student_data = {}
            student_data['soStudentId'] = student['id']
            student_data['soStudentName'] = student['name']
            student_data['avt_student'] = student['avt']
            list_student_checkin.append(student_data)
        return Response(list_student_checkin, status=200)
    

class get_checkout_class(APIView):
    def get(self, request):
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response({"error": "Vui lòng cung cấp ID lớp học."}, status=400)
        today = datetime.today().date()
        start = datetime.combine(today, datetime.min.time())  # 00:00:00
        end = datetime.combine(today, datetime.max.time())    # 23:59:59.999999

        # print(today)
        checkin = SoCheckins.objects.filter(soClassesId=class_id, checkDate__range=(start, end), checkType = 'in')
        checkin_serializer = SoCheckinsSerializer(checkin, many=True)
        checkin_studenId = [item['soStudentId'] for item in checkin_serializer.data]
        checkout = SoCheckins.objects.filter(soClassesId=class_id, checkDate__range=(start, end), checkType = 'out')
        checkout_serializer = SoCheckinsSerializer(checkout, many=True)
        checkout_studenId = [item['soStudentId'] for item in checkout_serializer.data]
        # print(checkin_studenId)
        list_student_checkout = SoStudent.objects.filter(id__in=checkin_studenId).exclude(id__in=checkout_studenId)
        serializer_student = SoStudentsSerializer(list_student_checkout, many=True)
        list_student_checkout = []
        for student in serializer_student.data:
            student_data = {}
            student_data['soStudentId'] = student['id']
            student_data['soStudentName'] = student['name']
            student_data['avt_student'] = student['avt']
            list_student_checkout.append(student_data)
        return Response(list_student_checkout, status=200)
    
class get_detail_student_within_permission(APIView):
    def get(self, request):
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response({"error": "Vui lòng cung cấp ID lớp học."}, status=400)
        total_with_permission,_,_ = Get_Detail_Class().get_student_attendance_count(class_id)
        serializer_studentOff = SoStudentOffSerializer(total_with_permission, many=True)
        checkout_ids = [item['soStudentId'] for item in serializer_studentOff.data]
        student_info = SoStudent.objects.filter(id__in=checkout_ids)
        # print(student_info)
        student_serializer = SoStudentsSerializer(student_info, many=True)
        total_with_permission = []
        for student in student_serializer.data:
            student_data = {}
            student_data['soStudentId'] = student['id']
            student_data['soStudentName'] = student['name']
            total_with_permission.append(student_data)
        return Response(total_with_permission, status=200)
    
class get_detail_student_without_permission(APIView):
    def get(self, request):
        class_id = request.query_params.get('class_id')
        if not class_id:
            return Response({"error": "Vui lòng cung cấp ID lớp học."}, status=400)
        total_without_permission = Get_Detail_Class().get_total_without_permission(class_id)
        # print(total_without_permission)
        student_info = SoStudent.objects.filter(id__in=total_without_permission)
        student_serializer = SoStudentsSerializer(student_info, many=True)
        total_without_permission = []
        for student in student_serializer.data:
            # print(student['id'])
            student_data = {}
            student_data['soStudentId'] = student['id']
            student_data['soStudentName'] = student['name']
            total_without_permission.append(student_data)
        return Response(total_without_permission, status=200)
    
class info_user(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        result = veriry_token(auth_header)
        payload = result.get('payload')
        user = SoUser.objects.filter(id=payload.get("user_id")).first()
        if not user:
            return Response({'error': 'Người dùng không tồn tại'}, status=404)
        user_serializer = SoUserSerializer(user)
        user_data = user_serializer.data
        # Chuyển chuỗi JSON thành list
        role_ids = json.loads(user_data['soRoleIds'])

        # Lấy thông tin từng vai trò
        roles_id = []
        roles_name = []
        for role_id in role_ids:
            role_obj = SoRole.objects.filter(id=role_id).first()
            if role_obj:
                role_serializer = SoRoleSerializer(role_obj)
                roles_id.append(role_serializer.data['id']) 
                roles_name.append(role_serializer.data['name'])

        user_data['soRoleIds'] = roles_id
        user_data['soRoleNames'] = roles_name
        user_data.pop('name_roles', None) 
        return Response({
            'user': user_data,
        }, status=200)
        

class score_student(APIView):
    def post(self, request):
        subject_id = request.data.get('subject_id')
        score_list = request.data.get('score')  # danh sách các loại điểm
        class_id = request.data.get('class_id')
        student_id = request.data.get('student_id')

        if not all([student_id, subject_id, score_list, class_id]):
            return Response({"error": "Thiếu tham số bắt buộc"}, status=400)

        today = date.today()
        hocKy_now = HocKy.objects.filter(start_date__lte=today, end_date__gte=today).first()
        if not hocKy_now:
            return Response({"error": "Không có học kỳ hiện tại"}, status=404)

        diem = Diem.objects.filter(
            soStudentId=student_id,
            subject_id=subject_id,
            hoc_ky_id=hocKy_now.id
        ).first()

        if not diem:
            # Chưa có -> tạo mới
            object_score = {
                "soStudentId": student_id,
                "subject_id": subject_id,
                "hoc_ky_id": hocKy_now.id,
                "soClassesId": class_id,
            }

            for sc in score_list:
                object_score[sc['type_score']] = sc['score']

            serializer = DiemSerializer(data=object_score)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)

        else:
            # Đã có -> cập nhật
            for sc in score_list:
                type_score = sc['type_score']
                new_score = sc['score']

                if not hasattr(diem, type_score):
                    return Response({"error": f"Trường {type_score} không tồn tại"}, status=400)

                current_scores = getattr(diem, type_score) or []

                # Trường hợp current_scores là chuỗi JSON:
                # if isinstance(current_scores, str):
                try:
                    current_scores = json.loads(current_scores)
                except:
                    current_scores = []
                # print(new_score)
                # # Nếu là số mới, thì biến thành list để append
                # if not isinstance(current_scores, list):
                current_scores = new_score

                # # Append nếu new_score là list hoặc số
                # if isinstance(new_score, list):
                #     current_scores.extend(new_score)
                # else:
                #     current_scores.append(new_score)

                setattr(diem, type_score, current_scores)

            diem.save()
            return Response(DiemSerializer(diem).data, status=200)


    def get(self, request):
        class_id = request.query_params.get('class_id')
        user_id = request.query_params.get('user_id')
        student_id = request.query_params.get('student_id')
        if not class_id:
            return Response({"error": "Vui lòng cung cấp ID lớp học."}, status=400)
        if not user_id:
            return Response({"error": "Vui lòng cung cấp ID giáo viên."}, status=400)

        today = date.today()
        hocKy_now = HocKy.objects.filter(start_date__lte=today, end_date__gte=today).first()
        if not hocKy_now:
            return Response({"error": "Không có học kỳ nào trong khoảng thời gian này."}, status=400)

        teacher_role = TeacherRole.objects.filter(user_id=user_id).first()
        if not teacher_role:
            return Response({"error": "Người dùng không có vai trò giáo viên."}, status=400)

        student = SoStudent.objects.filter(id=student_id).first()
        # if not students.exists():
        #     return Response({"error": "Không có học sinh nào trong lớp này."}, status=400)

        result = []

        
        student_data = {
            "id": student.id,
            "name": student.name,
            "subjects": []
        }

        # Xác định các môn dạy tương ứng
        if teacher_role.role_type == 'homeroom':
            subjects = Subject.objects.filter(taught_by='homeroom')
        else:
            user_subjects = UserSubject.objects.filter(user_id=user_id)
            subjects = [Subject.objects.get(id=us.subject_id) for us in user_subjects]
        for subject in subjects:
            diem = Diem.objects.filter(
                soStudentId=student.id,
                subject_id=subject.id,
                hoc_ky_id=hocKy_now.id
            ).first()
            print(diem)
            if diem:
                diem_serializer = DiemSerializer(diem)
                subject_data = {
                    "subjectId": subject.id,
                    "subjectName": subject.name,
                    "diem_15p": diem_serializer.data.get("diem_15p"),
                    "diem_mieng":diem_serializer.data.get("diem_mieng"),
                    "diem_1t": diem_serializer.data.get("diem_1tiet"),
                    "diem_hk": diem_serializer.data.get("diem_hk"),
                    "diem_tb": diem_serializer.data.get("diem_tb")
                }
            else:
                subject_data = {
                    "subjectId": subject.id,
                    "subjectName": subject.name,
                    "diem_mieng":None,
                    "diem_15p": None,
                    "diem_1t": None,
                    "diem_hk": None,
                    "diem_tb": None
                }

            student_data["subjects"].append(subject_data)

        result.append(student_data)

        return Response(result, status=200)

