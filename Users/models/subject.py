from django.db import models

class Subject(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    taught_by = models.CharField(max_length=100)
    class Meta:
        managed = False  # Tạo bảng này từ cơ sở dữ liệu hiện tại, không tạo mới.
        db_table = 'subject'
    def __str__(self):
        return self.name