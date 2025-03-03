from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    equipment = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.location})"

