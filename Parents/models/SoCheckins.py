from django.db import models
from Users.models.base import BaseModel
from Students.models.SoStudents import SoStudent
import uuid

class SoCheckins(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='id'
    )
    # id =  models.CharField(primary_key=True,max_length=512, db_column='id')
    checkType = models.CharField(max_length=50)
    checkDate = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    # soStudentId = models.ForeignKey(SoStudent, on_delete=models.CASCADE, related_name='checkins')
    # soClassesId = models.ForeignKey(SoClasses, on_delete=models.CASCADE, related_name='checkins')
    soStudentId = models.CharField(max_length=512, db_column='soStudentId') 
    soClassesId = models.CharField(max_length=512, db_column='soClassesId') 
    class Meta:
        managed = False          # Django sẽ không quản lý bảng này
        db_table = 'socheckins'  
    def __str__(self):
        return f"{self.soStudentId} - {self.checkType} ({self.checkDate})"
