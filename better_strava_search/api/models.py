from django.db import models


# Create your models here.
class Activity(models.Model):
    id = models.IntegerField(primary_key=True)
    start_date = models.DateTimeField()
    elapsed_time = models.FloatField()
    type = models.TextField()
    average_speed = models.FloatField()
    max_speed = models.FloatField()
    average_cadence = models.FloatField()
    average_heartrate = models.FloatField()
    max_heartrate = models.FloatField()
    suffer_score = models.FloatField()
    calories = models.FloatField()
    gear_name = models.TextField()
    description = models.TextField()
    distance = models.FloatField()
    name = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'activities'
