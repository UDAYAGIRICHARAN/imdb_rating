from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    language = models.CharField(max_length=50)
    rating = models.FloatField()
    description = models.TextField()
    budget = models.FloatField(default=0.0)
    revenue = models.FloatField(default=0.0)
    runtime = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Released')

    def __str__(self):
        return self.title