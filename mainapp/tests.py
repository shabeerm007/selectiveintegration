from django.test import TestCase

# Create your tests here.

from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your tests here.
dict = {'4': ['Ben deposited $425 in a savings account for 5 years at 7% simple interest per annum. What is the total interest he got?',
			 '$148.75','$168.25','$175','$80.75', 'choice1'],
		'2': ['''Josh bought 30 m of cloth at $5 a metre. Josh has only $20 notes. How many notes will he need to pay for the cloth?''',
			 '7','8','9','10', 'choice2'],
		'3':['The volume of a cube is 125 cm³. What is the total surface area of the cube?', '625 cm2',
			'250cm2','125cm2','150cm2','choice4'],
		'1':['How many ways can you rearrange the letters in the word ACCUMULATE so that the vowels are always together?',
			'10800','10500','12930','8100','choice1'],
		'5':['A coin is tossed 5 times. Find out the number of possible outcomes', 
			'8','16','32','64','choice3'],
	
		}
def unittest(request,*args, **kwargs):
    for key,item in dict.items():
        obj =  Maths()
        obj.que = item[0]
        obj.ch1,obj.ch2,obj.ch3,obj.ch4 = item[1],item[2],item[3],item[4] 
        obj.ans = item[5]
        obj.work = f'Workout for Question_{key}'
        obj.valid = False
        print(f"In unit testi \n {obj.que} ")
        obj.save()

    return render(request,"result.html",{'result':' database populated with 5 Q'})
'''

def unittest(request,*args, **kwargs):

	for key,item in dict.items():
		obj =  Question(id=key)
		obj.sub = 'Maths'
		obj.dif = 'Easy'
		obj.que = item[0]
		obj.ch1,obj.ch2,obj.ch3,obj.ch4 = item[1],item[2],item[3],item[4]
		obj.ans = item[5]
		obj.work = f'Workout for Question_{key}'
		obj.valid = False
		obj.vaby = 'shabeer'
		obj.save()

	return render(request,"result.html",{'result':' database populated with 100 Q'})

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
'''
