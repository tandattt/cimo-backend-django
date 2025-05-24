from Users.models.base import BaseModel
from django.db import models
class SoClasses(BaseModel):
    id = models.CharField(primary_key=True,max_length=512, db_column='id') 
    name = models.CharField(max_length=255)
    # so_users = models.ManyToManyField('SoUser', through='SoClassUsers', related_name="classes")
    class Meta:
        managed = False          # Django sẽ không quản lý bảng này
        db_table = 'soclasses'     # <-- Tên chính xác bảng đang tồn tại trong DB của bạn
    def __str__(self):
        return self.name
