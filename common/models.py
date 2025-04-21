from django.db import models
from django.utils import timezone

# Create your models here.
class Predictions(models.Model):
    date = models.DateField()
    flood_probability = models.FloatField(null=True, blank=True)
    drought_probability = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Predictions for {self.date}"