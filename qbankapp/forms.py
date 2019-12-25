from mainapp.models import Maths, English, GeneralA
from django.forms import ModelForm

class MathsForm(ModelForm):
	class Meta:
		model=Maths
		fields= ['que','ch1', 'ch2','ch3','ch4' ,
		'ans', 'wor', 'valid']

class EnglishForm(ModelForm):
	class Meta:
		model=English
		fields= ['que','ch1', 'ch2','ch3','ch4' ,
		'ans', 'wor', 'valid']

class GeneralAForm(ModelForm):
	class Meta:
		model=GeneralA
		fields= ['que','ch1', 'ch2','ch3','ch4' ,
		'ans', 'wor', 'valid']