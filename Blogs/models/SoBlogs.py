from django.db import models
from Users.models.base import BaseModel

class SoBlogs(BaseModel):
    id = models.CharField(primary_key=True,max_length=512, db_column='id') 
    name = models.CharField(max_length=255)
    sumary = models.TextField(null=True, blank=True)
    imgs = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    relateIds = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        managed = False          # Django sẽ không quản lý bảng này
        db_table = 'soblogs'     # <-- Tên chính xác bảng đang tồn tại trong DB của bạn
    def __str__(self):
        return self.name
