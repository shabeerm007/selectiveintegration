from django.db import models

# Create your models here.
class Question(models.Model):
	sub 	= models.CharField(max_length=10)
	dif 	= models.CharField(max_length=10)
	que 	= models.TextField()
	ch1 	= models.CharField(max_length=10)
	ch2 	= models.CharField(max_length=10)
	ch3 	= models.CharField(max_length=10)
	ch4 	= models.CharField(max_length=10)
	ans     = models.CharField(max_length=2)
	wor 	= models.TextField()
	valid 	= models.BooleanField()
	vaby	= models.CharField(max_length=10)
