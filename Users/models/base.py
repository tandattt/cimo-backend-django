import uuid
from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isDeleted = models.BooleanField(default=False)

    createdBy = models.CharField(max_length=255, null=True, blank=True)
    updatedBy = models.CharField(max_length=255, null=True, blank=True)

    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
