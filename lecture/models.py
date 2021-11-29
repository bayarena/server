from django.db import models
from motivator.models import Motivator

class Lecture(models.Model):
	class Meta:
		ordering = ['date']

	title = models.CharField(max_length=70)
	date = models.DateTimeField()
	image = models.ImageField(null=True)

	category = models.CharField(max_length=70, blank=True)
	description = models.CharField(max_length=300, blank=True)
	theme = models.CharField(max_length=70, blank=True)
	time = models.IntegerField(default=0)
	difficulty = models.IntegerField(default=0)

	motivators = models.ManyToManyField(Motivator)