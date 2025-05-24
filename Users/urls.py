# Parents/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
# from .views import SoCheckinsViewSet, 
# process_leave_request
from .views import (Bot_TimetableAPIView, CheckinAPIView, TimetableAPIView,Get_List_Class,Get_Detail_Class, StudentOffAPI
,get_checkin_class,get_checkout_class, get_detail_student_within_permission,get_detail_student_without_permission,info_user,
score_student)
# router = DefaultRouter()
# router.register(r'checkins', SoCheckinsViewSet)

urlpatterns =[
    # path('', include(router.urls)),  # sử dụng router thay vì DefaultRouter
    path('bot_check_timetable/', Bot_TimetableAPIView.as_view()),
    path('checkin/', CheckinAPIView.as_view()),
    path('timetable/', TimetableAPIView.as_view()),
    path('get_List_Class/', Get_List_Class.as_view()),
    path('get_Detail_Class/', Get_Detail_Class.as_view()),
    path('update_leave/',StudentOffAPI.as_view()),
    path('get_checkin_class/',get_checkin_class.as_view()),
    path('get_checkout_class/',get_checkout_class.as_view()),
    path('get_detail_student_within_permission/',get_detail_student_within_permission.as_view()),
    path('get_detail_student_without_permission/',get_detail_student_without_permission.as_view()),
    path('me/',info_user.as_view()),
    path('score_student/',score_student.as_view()),
]
