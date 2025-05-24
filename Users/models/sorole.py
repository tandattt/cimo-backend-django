from .base import BaseModel
from django.db import models
class SoRole(BaseModel):
    id = models.CharField(primary_key=True,max_length=512, db_column='id') 
    name = models.CharField(max_length=255)
    class Meta:
        managed = False          # Django sẽ không quản lý bảng này
        db_table = 'sorole'
    def __str__(self):
        return self.name
