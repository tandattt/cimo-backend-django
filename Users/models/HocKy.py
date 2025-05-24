
from django.db import models
import uuid

class HocKy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ten_hoc_ky = models.CharField(max_length=20)
    nam_hoc = models.CharField(max_length=9)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'hocky'

    def __str__(self):
        return f"{self.ten_hoc_ky} - {self.nam_hoc}"
