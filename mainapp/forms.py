
from django import forms
from mainapp.models import *

class ExamForm(forms.Form):

  def __init__(self, *args,**kwargs):

    if 'choices' in kwargs:
      choicelist = kwargs.pop('choices')
    else:
      #We should reach this section when only to validate the form
      choicelist=[]
    super().__init__(*args, **kwargs)
    self.fields['selectedchoice'] = forms.CharField(label ='',widget=forms.RadioSelect(choices=choicelist))