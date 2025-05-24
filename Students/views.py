from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import datetime
from .models.SoStudents import SoStudent
from .models.SoStudentOff import SoStudentOff
from rest_framework.parsers import MultiPartParser, FormParser
from Parents.models import SoCheckins,SoParents,SoStudentParents
from Students.serializers.so_classes_serializer import SoClassesSerializer
from Students.serializers.so_class_users_serializer import SoClassUsersSerializer
from .serializers.so_student_off_serializer import SoStudentOffSerializer
from Students.models.SoClasses import SoClasses
from Students.models.SoClassUsers import SoClassUserss
from Users.models import SoUser
from Users.serializers import SoUserSerializer
from collections import defaultdict
from Auth.views import veriry_token
import calendar
from drf_yasg.utils import swagger_auto_schema
from uuid import uuid4
import os
from Cimo import settings
from datetime import timedelta,date
from Users.models.HocKy import HocKy
from Users.models.Diem import Diem
from Users.serializers.Diem_serializer import DiemSerializer
from Users.models.subject import Subject
class AttendanceAPI(APIView):
    def get(self, request):
        student_id = request.query_params.get('studentId')
        month_str = request.query_params.get('month')  # dạng '2025-04'

        if not student_id or not month_str:
            return Response({'error': 'Thiếu studentId hoặc month'}, status=400)

        try:
            # Parse tháng đầu và cuối trong tháng
            year, month = map(int, month_str.split('-'))
            first_day = datetime(year, month, 1)
            last_day = datetime(year, month, calendar.monthrange(year, month)[1])
        except:
            return Response({'error': 'Định dạng tháng không hợp lệ. VD: 2025-04'}, status=400)
        # student_id = UUID(student_id_str)
        checkins = SoCheckins.objects.filter(
            soStudentId=student_id,
            checkDate__date__gte=first_day.date(),
            checkDate__date__lte=last_day.date()
        ).order_by('checkDate')
        # print(checkins)
        result_by_date = defaultdict(dict)

        for check in checkins:
            date_str = check.checkDate.strftime('%Y-%m-%d')
            check_data = {
                'id': str(check.id),
                'checkDate': check.checkDate.isoformat(),
                'createdBy': check.createdBy,
                'checkType': check.checkType,
                'note': check.note,
                'soClassId': str(check.soClassesId),
                'soStudentId': str(check.soStudentId),
            }
            result_by_date[date_str][check.checkType] = check_data

        # Duyệt từ ngày 1 đến hết tháng để lấp đầy đủ ngày
        result = []
        current_date = first_day
        while current_date <= last_day:
            date_str = current_date.strftime('%Y-%m-%d')
            checks = result_by_date.get(date_str, {})
            
            item = {'date': date_str}
            if checks:  # chỉ thêm khi có dữ liệu checkin/out
                if 'in' in checks:
                    item['checkin'] = checks['in']
                if 'out' in checks:
                    item['checkout'] = checks['out']

            result.append(item)
            current_date += timedelta(days=1)
        return Response(result, status=200)

class Bot_AttendanceAPI(APIView):
    #dùng cho bot
    def post(self, request, *args, **kwargs):
        data = request.data
        student_name = data.get('student_name')
        sender_id = data.get('sender_id')
        # print(sender_id)
        # print(student_name)
        if not student_name:
            return Response({"error": "Vui lòng cung cấp tên học sinh."}, status=400)
        list_checkin = []
        for i in student_name:
            # print(i)
            student_parents = SoStudentParents.objects.filter(soParentid=sender_id)
            if not student_parents.exists():
                # print(i)
                return Response({"message": f"bạn không có con tên là '{i}'"}, status=404)
            student_main = None
            # print(student_parents)
            # print(i)
            for student_parent in student_parents:
                # print(student_parent)
                student = SoStudent.objects.filter(id=student_parent.soStudentid, name=i).first()
                # print(student_parent.soStudentid)
                # print(student)
                if not student:
                    # return Response({"message": f"không có học sinh {i}"}, status=400)
                    continue
                student_main = student
                break
                
            # print(student_main.id)
            attendance_records = SoCheckins.objects.filter(soStudentId=student_main.id)
            # print(attendance_records)
            if not attendance_records.exists():
                return Response({"message": f"Học sinh '{i}' chưa có dữ liệu điểm danh."}, status=400)

            
            listUser = []
            for record in attendance_records:
                so_class = SoClasses.objects.filter(id=record.soClassesId).first()
                # print(record.soClassesId)
                # print(so_class.id)
                class_serializer = SoClassesSerializer(so_class)  # Lấy tên lớp học
                soUserClasses = SoClassUserss.objects.filter(soClassId=so_class.id)
            # print(soUserClasses)
                # print(listUser)
                list_checkin.append({
                    "name": i,
                    "check_in": record.checkDate.strftime("%Y-%m-%d %H:%M:%S"),  # Chuyển định dạng thời gian
                    "class": class_serializer.data['name'],
                    "teacher": listUser,
                    "note": record.note if record.note else "Không có ghi chú"
                })
                # print(list_checkin)
            
            if soUserClasses.exists():
                for soUserClass in soUserClasses:
                    # print(soUserClass.soUserId)
                    soUser = SoUser.objects.filter(id=soUserClass.soUserId).first()
                    # print(soUser)
                    soUsersSerializer = SoUserSerializer(soUser)
                    # print(soUsersSerializer.data)
                    listUser.append(soUsersSerializer.data['name'])
        # print(list_checkin)
        return Response(list_checkin, status=200)


class StudentOffGetByClassAPI(APIView):
    def get(self, request):
        class_id = request.query_params.get('soClassId')
        
        studentOff = SoStudentOff.objects.filter(soClassId=class_id).order_by('createdDate')        
        serializer = SoStudentOffSerializer(studentOff, many=True)
        return Response({"data": serializer.data}, status=200)
    
class StudentOffGetByStudentAndParentAPI(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        payload = veriry_token(auth_header)
        student_id = request.query_params.get('soStudentId')
        parent_id = payload.get("payload").get("parent")
        print(student_id)
        print(parent_id)
        studentOff = SoStudentOff.objects.filter(soStudentId=student_id, soParentId=parent_id).order_by('createdDate')
        if not studentOff.exists():
            return Response({'error': 'Không tìm thấy dữ liệu nghỉ học'}, status=403)
        return Response({"data": studentOff.values()}, status=200)
    
    
class StudentOffAPI(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        result = veriry_token(auth_header)

        if not result.get("valid"):
            return Response({"error": result.get("error")}, status=401)

        student_off_id = request.query_params.get('studentOffId')
        if not student_off_id:
            return Response({"error": "Thiếu studentOffId"}, status=400)

        studentOff = SoStudentOff.objects.filter(id=student_off_id).first()
        if not studentOff:
            return Response({"error": "Không tìm thấy dữ liệu"}, status=404)

        serializer = SoStudentOffSerializer(studentOff)
        return Response({"data": serializer.data}, status=200)
    # @swagger_auto_schema(request_body=SoStudentOffSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        auth_header = request.headers.get('Authorization')
        result = veriry_token(auth_header)

        if not result.get("valid"):
            return Response({"error": result.get("error")}, status=401)

        serializer = SoStudentOffSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "success","data": serializer.data}, status=201)
        else:
            return Response({"error": serializer.errors}, status=400)

            
urls = 'https://cimoo.duckdns.org/cimo-django'
class UploadAvtApi(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        student_id = request.data.get('studentId')
        avt_file = request.FILES.get('avt')

        if not student_id or not avt_file:
            return Response({'error': 'Thiếu studentId hoặc avt'}, status=400)

        try:
            student = SoStudent.objects.get(id=student_id)

            # tạo tên file an toàn và duy nhất
            ext = os.path.splitext(avt_file.name)[-1]
            filename = f"{uuid4().hex}{ext}"
            folder_path = os.path.join(settings.MEDIA_ROOT, "images")
            os.makedirs(folder_path, exist_ok=True)
            filepath = os.path.join(folder_path, filename)
            print(filename)
            # ghi file vào thư mục
            with open(filepath, 'wb+') as destination:
                for chunk in avt_file.chunks():
                    destination.write(chunk)

            # lưu URL vào DB
            full_url = f"{urls}{settings.MEDIA_URL}images/{filename}"
            # full_url = request.build_absolute_uri(relative_url)  # ✅ dòng mới
            # print(request.build_absolute_uri)
            print(full_url)
            # print(relative_url)
            student.avt = full_url
            student.save()

            return Response({'message': 'Upload thành công', 'avatar_url': full_url}, status=200)

        except SoStudent.DoesNotExist:
            return Response({'error': 'Học sinh không tồn tại'}, status=404)
        
        
class Get_Score_Student(APIView):
    def get(self, request):
        student_id = request.query_params.get('studentId')
        if not student_id:
            return Response({'error': 'Thiếu studentId'}, status=400)
        today = date.today()
        hocKy_now = HocKy.objects.filter(start_date__lte=today, end_date__gte=today).first()
        if not hocKy_now:
            return Response({"error": "Không có học kỳ nào trong khoảng thời gian này."}, status=400)
        subiects = Subject.objects.filter().all()
        result = []
        for subject in subiects:
            
            # print(subject.id)
            # print(subject.name)
            score = Diem.objects.filter(soStudentId=student_id, hoc_ky_id = hocKy_now.id, subject_id = subject.id).first()
            if score:
                diem_serializer = DiemSerializer(score)
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
            result.append(subject_data)
        return Response(result, status=200)