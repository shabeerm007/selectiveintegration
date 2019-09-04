from django.test import TestCase

# Create your tests here.

from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

# Create your tests here.


def unittest(request,*args, **kwargs):

	for i in range(1,101):
		obj =  Question()
		obj.sub = 'Maths'
		obj.dif = 'Easy'
		obj.que = f'Question_{i}'
		obj.ch1,obj.ch2,obj.ch3,obj.ch4 = i*5+1,i*5+2,i*5+3,i*5+4,
		obj.ans = 'a'
		obj.work = f'Workout for Question_{i}'
		obj.valid = False
		obj.vaby = 'shabeer'
		obj.save()

	return render(request,"result.html",{'result':' database populated with 100 Q'})
