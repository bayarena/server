from django.db import models

class Motivator(models.Model):
	name_eng = models.CharField(max_length=70)
	name_kor = models.CharField(max_length=70)

	image = models.ImageField(null=True)
	image_thumb = models.ImageField(null=True)

