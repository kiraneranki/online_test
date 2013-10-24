from django.db import models

# Create your models here.

class SpokenTutorialDetail(models.Model):
    """ Spoken Tutorial User details """
    user_id = models.IntegerField()
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    foss = models.CharField(max_length=60)
    testcode = models.CharField(max_length=20)
    status = models.CharField(max_length=10)
    result = models.FloatField()
    result_status = models.CharField(max_length=10)
    date_added = models.DateField()
