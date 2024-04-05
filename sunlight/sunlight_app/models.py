from django.db import models


class Program(models.Model):
    name = models.CharField(max_length=256)
    wake_time = models.TimeField()
    
    def __str__(self):
        return self.name
