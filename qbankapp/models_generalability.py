from django.db import models
from django.urls import reverse
from .models import QContext

class GeneralA(models.Model):
	que 	= models.TextField(max_length=5*1024) 					#Question
	ch1 	= models.CharField(max_length=100)						#Choice1
	ch2 	= models.CharField(max_length=100)						#Choice2
	ch3 	= models.CharField(max_length=100)						#Choice3
	ch4 	= models.CharField(max_length=100)						#Choice4
	ans     = models.CharField(max_length=10)						#Answer
	wor 	= models.TextField()									#Working out
	valid 	= models.BooleanField()									#Vallid question or not
	context = models.ForeignKey(QContext, null=True, blank=True, default=None, \
								on_delete=models.CASCADE, \
								verbose_name='question context')
	def __str__(self):
		return f"GeneralA: Question Number - {self.pk}"

	def to_dict(self):
		return {'Pk'		:self.pk,
				'Question'	:self.que,
				'Choice 1'	:self.ch1,
				'Choice 2'	:self.ch2,
				'Choice 3'	:self.ch3,
				'Choice 4'	:self.ch4,
				'Answer'  	:self.ans,
				'Solution'	:self.wor,
				'Validated'	:self.valid,
				}

	def get_absolute_url(self):
		return reverse('detail-generalability',kwargs={'pk':self.pk})
