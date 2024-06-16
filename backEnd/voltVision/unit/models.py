from django.db import models

# Create your models here.

from django.db import models

class Unit(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    time_date = models.DateField()
    watt = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.time_date} - {self.watt}"