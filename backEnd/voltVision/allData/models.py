from django.db import models


class AllData(models.Model):
    id = models.AutoField(primary_key=True)
    unit_id = models.CharField(max_length=255)
    time_date = models.DateTimeField()
    volt = models.DecimalField(max_digits=5, decimal_places=2)
    amp = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"ID: {self.id}, Unit: {self.unit_id}, Voltage: {self.volt}V, Current: {self.amp}A, Date: {self.time_date}"
