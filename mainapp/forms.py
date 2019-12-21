
from django import forms
from mainapp.models import Maths,English,GeneralA


class ExamForm(forms.Form):

  def __init__(self, *args,**kwargs):

    if 'choices' in kwargs:
      choicelist = kwargs.pop('choices')
    else:
      #We should reach this section when only to validate the form
      choicelist=[]
    super().__init__(*args, **kwargs)
    self.fields['selectedchoice'] = forms.CharField(label ='',widget=forms.RadioSelect(choices=choicelist))

class ContactForm(forms.Form):
	name = forms.CharField(label='Name', max_length =100)
	email = forms.EmailField()
	phone = forms.DecimalField(max_digits=10)
	subject = forms.CharField(label='subject', max_length =500)
	message = forms.CharField(widget=forms.Textarea)

