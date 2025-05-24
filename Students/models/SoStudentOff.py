from django.db import models
from .SoStudents import SoStudent
from Parents.models import SoParents
from Users.models.base import BaseModel

class SoStudentOff(BaseModel):
    # student = models.ForeignKey(SoStudent, on_delete=models.CASCADE, related_name='student_offs')
    # parent = models.ForeignKey(SoParents, on_delete=models.CASCADE, related_name='student_offs')
    soStudentId = models.CharField(max_length=512, db_column='student_id') 
    soParentId = models.CharField(max_length=512, db_column='parent_id') 
    soClassId = models.CharField(max_length=512, db_column='class_id')
    soUserId = models.CharField(max_length=36, db_column='approved_by')
    leaveStartDate = models.DateField(db_column='start_date')
    leaveEndDate = models.DateField(db_column='end_date')

    reason = models.TextField()
    note = models.TextField(blank=True, null=True)
    # approved_by =models.CharField(max_length=36,db_column='approved_by')
    leaveStatus = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending',db_column='status')
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)
    createdBy = models.CharField(max_length=512, db_column='createdBy')
    updatedBy = models.CharField(max_length=512, db_column='updatedBy')
    class Meta:
        managed = False          # Django sẽ không quản lý bảng này
        db_table = 'so_student_off'     # <-- Tên chính xác bảng đang tồn tại trong DB của bạn
    def __str__(self):
        return f"{self.soStudentId} - {self.leaveStartDate} to {self.leaveEndDate} ({self.leaveStatus})"
