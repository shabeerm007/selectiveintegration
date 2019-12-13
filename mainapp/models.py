from django.db import models

class Maths(models.Model):
	que 	= models.TextField(max_length=5*1024) 				#Question
	ch1 	= models.CharField(max_length=10)	#Choice1
	ch2 	= models.CharField(max_length=10)	#Choice2
	ch3 	= models.CharField(max_length=10)	#Choice3
	ch4 	= models.CharField(max_length=10)	#Choice4
	ans     = models.CharField(max_length=10)	#Answer
	wor 	= models.TextField()				#Working out
	valid 	= models.BooleanField()				#Vallid question or not

class English(models.Model):
	que = models.TextField(max_length=5*1024) 					#Question
	ch1 	= models.CharField(max_length=10)	#Choice1
	ch2 	= models.CharField(max_length=10)	#Choice2
	ch3 	= models.CharField(max_length=10)	#Choice3
	ch4 	= models.CharField(max_length=10)	#Choice4
	ans     = models.CharField(max_length=10)	#Answer
	wor 	= models.TextField()				#Working out
	valid 	= models.BooleanField()				#Vallid question or not

class GeneralA(models.Model):
	que = models.TextField(max_length=5*1024) 					#Question
	ch1 	= models.CharField(max_length=10)	#Choice1
	ch2 	= models.CharField(max_length=10)	#Choice2
	ch3 	= models.CharField(max_length=10)	#Choice3
	ch4 	= models.CharField(max_length=10)	#Choice4
	ans     = models.CharField(max_length=10)	#Answer
	wor 	= models.TextField()				#Working out
	valid 	= models.BooleanField()				#Vallid question or not

