from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.date} {self.time}"