from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.department})"

