from Users.models.base import BaseModel
from django.db import models
# from .SoClasses import SoClasses
class SoStudent(BaseModel):
    id = models.CharField(primary_key=True,max_length=512, db_column='id') 
    name = models.CharField(max_length=255)
    dob = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    nationalId = models.CharField(max_length=20, null=True, blank=True)
    avt = models.CharField(max_length=255, null=True, blank=True)

    # soClassId = models.IntegerField(db_column='soClassId')
    soClassId = models.CharField(max_length=512, db_column='soClassId') 
    class Meta:
        managed = False          # Django sẽ không quản lý bảng này
        db_table = 'sostudent'     # <-- Tên chính xác bảng đang tồn tại trong DB của bạn
    def __str__(self):
        return self.name
