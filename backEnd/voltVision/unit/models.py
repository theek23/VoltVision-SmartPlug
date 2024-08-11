from django.db import models

from user.models import User


class Unit(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='units')
    place = models.CharField(max_length=255)

    def __str__(self):
        return f"Unit ID: {self.id}, Place: {self.place}"
