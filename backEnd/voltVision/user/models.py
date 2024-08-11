from django.db import models


class User(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email
