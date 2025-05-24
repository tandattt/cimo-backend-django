from .base import BaseModel
from django.db import models
from .sorole import SoRole

class SoUser(BaseModel):
    id = models.CharField(primary_key=True,max_length=512, db_column='id') 
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    dob = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    avt = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    nationalId = models.CharField(max_length=20, null=True, blank=True)

    soRoleIds = models.CharField(max_length=512, db_column='soRoleIds')
    
    class Meta:
        managed = False          # Django sẽ không quản lý bảng này
        db_table = 'souser'

    def __str__(self):
        return self.username
