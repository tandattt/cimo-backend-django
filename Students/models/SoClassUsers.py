from django.db import models
from Users.models.base import BaseModel

class SoClassUserss(BaseModel):
    # soClassId = models.ForeignKey(SoClasses, on_delete=models.CASCADE, related_name='class_users')
    # soUserId = models.ForeignKey(SoUser, on_delete=models.CASCADE, related_name='user_classes')
    
    soClassId = models.CharField(max_length=512, db_column='soClassId') 
    soUserId = models.CharField(max_length=512, db_column='soUserId') 
    class Meta:
        managed = False          # Django sẽ không quản lý bảng này
        db_table = 'soclassusers'     # <-- Tên chính xác bảng đang tồn tại trong DB của bạn
    def __str__(self):
        return f"{self.soUserId} - {self.soClassId}"
