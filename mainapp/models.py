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

class Maths(models.Model):
	que 	= models.TextField(max_length = 5*1024) 				#Question
	ch1 	= models.CharField(max_length=10)	#Choice1
	ch2 	= models.CharField(max_length=10)	#Choice2
	ch3 	= models.CharField(max_length=10)	#Choice3
	ch4 	= models.CharField(max_length=10)	#Choice4
	ans     = models.CharField(max_length=2)	#Answer
	wor 	= models.TextField()				#Working out
	valid 	= models.BooleanField()				#Vallid question or not

class English(models.Model):
	que = models.TextField() 					#Question
	ch1 	= models.CharField(max_length=10)	#Choice1
	ch2 	= models.CharField(max_length=10)	#Choice2
	ch3 	= models.CharField(max_length=10)	#Choice3
	ch4 	= models.CharField(max_length=10)	#Choice4
	ans     = models.CharField(max_length=2)	#Answer
	wor 	= models.TextField()				#Working out
	valid 	= models.BooleanField()				#Vallid question or not

class GeneralA(models.Model):
	que = models.TextField() 					#Question
	ch1 	= models.CharField(max_length=10)	#Choice1
	ch2 	= models.CharField(max_length=10)	#Choice2
	ch3 	= models.CharField(max_length=10)	#Choice3
	ch4 	= models.CharField(max_length=10)	#Choice4
	ans     = models.CharField(max_length=2)	#Answer
	wor 	= models.TextField()				#Working out
	valid 	= models.BooleanField()				#Vallid question or not

