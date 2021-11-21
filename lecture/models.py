from django.db import models
from motivator.models import Motivator

class Lecture(models.Model):
	class Meta:
		ordering = ['date']

	title = models.CharField(max_length=70)
	subtitle = models.CharField(max_length=70)
	date = models.DateTimeField()
	image = models.ImageField(null=True)

	motivators = models.ManyToManyField(Motivator)