
from django.db import models
import uuid

class Diem(models.Model):
    id = models.CharField(max_length=36,primary_key=True, default=uuid.uuid4, editable=False)
    hoc_ky_id = models.CharField(max_length=36)  # giả sử UUID
    soStudentId = models.CharField(max_length=36)
    subject_id = models.CharField(max_length=36)
    soClassesId = models.CharField(max_length=36,db_column='soClasses_id')
    diem_15p = models.JSONField(null=True, blank=True)
    diem_mieng = models.JSONField(null=True, blank=True)
    diem_1tiet = models.JSONField(null=True, blank=True)
    diem_hk = models.FloatField(null=True, blank=True)
    diem_tb = models.FloatField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'diem'

    def __str__(self):
        return f"{self.soStudentId} - {self.subject_id} - {self.hoc_ky_id}"
