from django.db import models
from django.urls import reverse

class Maths(models.Model):
	que 	= models.TextField(max_length=5*1024) 					#Question
	ch1 	= models.CharField(max_length=100)						#Choice1
	ch2 	= models.CharField(max_length=100)						#Choice2
	ch3 	= models.CharField(max_length=100)						#Choice3
	ch4 	= models.CharField(max_length=100)						#Choice4
	ans     = models.CharField(max_length=10)						#Answer
	wor 	= models.TextField()									#Working out
	valid 	= models.BooleanField()									#Vallid question or not
	
	def __str__(self):
		return f"Maths: Question Number - {self.pk}"

	def to_dict(self):
		return {'Qnum': self.pk,
				'Question':self.que,
				'Choice 1':self.ch1,
				'Choice 2':self.ch2,
				'Choice 3':self.ch3,
				'Choice 4':self.ch4,
				'Answer'  :self.ans,
				'Solution':self.wor,
				'Validated':self.valid }

	
	def get_absolute_url(self):
		return reverse('list-maths') 								#Lists all contents of the table


class English(models.Model):
	que = models.TextField(max_length=5*1024) 						#Question
	ch1 	= models.CharField(max_length=100)						#Choice1
	ch2 	= models.CharField(max_length=100)						#Choice2
	ch3 	= models.CharField(max_length=100)						#Choice3
	ch4 	= models.CharField(max_length=100)						#Choice4
	ans     = models.CharField(max_length=10)						#Answer
	wor 	= models.TextField()									#Working out
	valid 	= models.BooleanField()									#Vallid question or not

	def __str__(self):
		return f"English: Question Number - {self.pk}"

	def to_dict(self):
		return {'Qnum': self.pk,
				'Question':self.que,
				'Choice 1':self.ch1,
				'Choice 2':self.ch2,
				'Choice 3':self.ch3,
				'Choice 4':self.ch4,
				'Answer'  :self.ans,
				'Solution':self.wor,
				'Validated':self.valid}

	def get_absolute_url(self):
		return reverse('list-eng') 									#Lists all contents of the table

class GeneralA(models.Model):
	que = models.TextField(max_length=5*1024) 						#Question
	ch1 	= models.CharField(max_length=100)						#Choice1
	ch2 	= models.CharField(max_length=100)						#Choice2
	ch3 	= models.CharField(max_length=100)						#Choice3
	ch4 	= models.CharField(max_length=100)						#Choice4
	ans     = models.CharField(max_length=10)						#Answer
	wor 	= models.TextField()									#Working out
	valid 	= models.BooleanField()									#Vallid question or not

	def __str__(self):
		return f"GeneralA: Question Number - {self.pk}"

	def to_dict(self):
		return {'Qnum': self.pk,
				'Question':self.que,
				'Choice 1':self.ch1,
				'Choice 2':self.ch2,
				'Choice 3':self.ch3,
				'Choice 4':self.ch4,
				'Answer'  :self.ans,
				'Solution':self.wor,
				'Validated':self.valid}

	def get_absolute_url(self):
		return reverse('list-ga') 									#Lists all contents of the table


