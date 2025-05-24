from django.db import models
from Students.models.SoStudents import SoStudent   # Import model Student từ app Students
from .SoParents import SoParents   # Import model Parent từ app Parents
from Users.models.base import BaseModel  # Import BaseModel nếu bạn có một base model chung

class SoStudentParents(BaseModel):
    soStudentid = models.CharField(max_length=512, db_column='soStudentid') 
    soParentid = models.CharField(max_length=512, db_column='soParentid')   

    class Meta:
        unique_together = ('soStudentid', 'soParentid')
        managed = False          # Django sẽ không quản lý bảng này
        db_table = 'sostudentparents'     # <-- Tên chính xác bảng đang tồn tại trong DB của bạn
    def __str__(self):
        return f"{self.soStudentid} - {self.soParentid}"
