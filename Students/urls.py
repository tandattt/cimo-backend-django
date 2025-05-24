# Parents/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
# from .views import SoCheckinsViewSet, 
# process_leave_request
from .views import AttendanceAPI, StudentOffGetByClassAPI, StudentOffGetByStudentAndParentAPI,StudentOffAPI, Bot_AttendanceAPI,UploadAvtApi, Get_Score_Student
# router.register(r'checkins', SoCheckinsViewSet)

urlpatterns =[
    # path('check_in/<uuid:student_id>/<str:month>/', AttendanceAPI.as_view(), name='attendance-by-month'),
    path('check_in/', AttendanceAPI.as_view()),
    path('bot_check_in/', Bot_AttendanceAPI.as_view()),
    path('student_off_get_by_class/', StudentOffGetByClassAPI.as_view()),
    path('student_off_get_by_student_and_parent/', StudentOffGetByStudentAndParentAPI.as_view()),
    path('StudentOffDetail/',StudentOffAPI.as_view()),
    path('upload_avt/',UploadAvtApi.as_view()),
    path('get_score_student/',Get_Score_Student.as_view())
]
