from django.db import models

class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.CharField(max_length=255,db_column='subject_id')
    teacher_id = models.CharField(max_length=255,db_column='teacher_id')
    class_id = models.CharField(max_length=255,db_column='class_id')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        managed = False  # Tạo bảng này từ cơ sở dữ liệu hiện tại, không tạo mới.
        db_table = 'timetable'
    def __str__(self):
        return f"{self.subject_id} - {self.teacher_id} - {self.class_id}"