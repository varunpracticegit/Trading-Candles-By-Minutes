# MainApp/models.py
from django.db import models

class Candle(models.Model):
    date = models.DateField()
    time = models.TimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return f'{self.date} {self.time}'
