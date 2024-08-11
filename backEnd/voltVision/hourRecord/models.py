from django.db import models


class HourRecord(models.Model):
    id = models.AutoField(primary_key=True)
    unit_id = models.CharField(max_length=255)
    off_start = models.DateTimeField()
    off_end = models.DateTimeField()
    off_duration = models.FloatField()
    on_start = models.DateTimeField()
    on_end = models.DateTimeField()
    on_duration = models.FloatField()
    watt = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"ID: {self.id}, Unit: {self.unit_id}, Watt: {self.watt}W, Off Duration: {self.off_duration}h, On Duration: {self.on_duration}h"
