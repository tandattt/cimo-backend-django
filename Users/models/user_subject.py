from django.db import models
from django.contrib.auth.models import User  # Giả sử `User` là bảng người dùng của Django

class UserSubject(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user_id = models.CharField(max_length=255)  # Liên kết với bảng user
    subject_id = models.CharField(max_length=255)  # Liên kết với bảng subject
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_subject'
        
    def __str__(self):
        return f"{self.user_id} - {self.subject_id}"
