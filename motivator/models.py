from django.db import models

class Motivator(models.Model):
	name_eng = models.CharField(max_length=70, blank=True)
	name_kor = models.CharField(max_length=70, blank=True)
	description = models.CharField(max_length=300, blank=True)
	expertise = models.CharField(max_length=70, blank=True)

	priority = models.IntegerField(default=-1)

	image = models.ImageField(null=True)
	image_thumb = models.ImageField(null=True)

