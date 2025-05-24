from django.db import models
from django.contrib.auth.models import User  # Giả sử `User` là bảng người dùng của Django

class TeacherRole(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user_id = models.CharField(max_length=255)  # Liên kết với bảng `souser` (giáo viên)
    role_type = models.CharField(max_length=50, choices=[('homeroom', 'Chủ Nhiệm'), ('subject_teacher', 'Giáo Viên Bộ Môn')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teacher_role'
        
    def __str__(self):
        return f"{self.user_id} - {self.role_type}"
