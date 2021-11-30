from django.db import models

class Category(models.Model):
	title = models.CharField(max_length=70)
	thumb = models.ImageField(null=True)