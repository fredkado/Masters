from django.db import models
from manage import init_django

init_django()

# define models here
class Solution(models.Model):
    chromosone = models.JSONField(default=dict(chromosone=[]))

class Fitness(models.Model):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    fitness_value = models.FloatField()    

