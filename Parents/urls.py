# Parents/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SoCheckinsViewSet, bot_process_leave_request,SoPerentsAPI, process_leave_request

router = DefaultRouter()
router.register(r'checkins', SoCheckinsViewSet)

urlpatterns =[
    path('', include(router.urls)),  # sử dụng router thay vì DefaultRouter
    path('bot_process-leave-request', bot_process_leave_request.as_view()),
    path('me',SoPerentsAPI.as_view()),
    path('process_leave_request',process_leave_request.as_view())
]
