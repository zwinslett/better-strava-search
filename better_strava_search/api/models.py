from django.db import models


# Create your models here.
class Activity(models.Model):
    id = models.IntegerField(primary_key=True)
    start_date = models.DateTimeField()
    elapsed_time = models.IntegerField()
    type = models.TextField()
    average_speed = models.IntegerField()
    max_speed = models.IntegerField()
    average_cadence = models.IntegerField()
    average_heartrate = models.IntegerField()
    max_heartrate = models.IntegerField()
    suffer_score = models.IntegerField()
    calories = models.IntegerField()
    gear_name = models.TextField()
    description = models.TextField()
    distance = models.IntegerField()
    name = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'activities'
