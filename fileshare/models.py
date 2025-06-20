from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('ops', 'Operation User'),
        ('client', 'Client User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    is_verified = models.BooleanField(default=False)

class UploadedFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
