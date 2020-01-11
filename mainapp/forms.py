
from django import forms
from mainapp.models import Maths,English,GeneralA
from django.utils.translation import gettext as _

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
  def __init__(self, *args,**kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name']= forms.CharField(label='Name', max_length =100)
    self.fields['email'] = forms.EmailField()
    self.fields['phone'] = forms.DecimalField(max_digits=10)
    self.fields['subject'] = forms.CharField(max_length =500)
    self.fields['message'] = forms.CharField(widget=forms.Textarea)

  def clean_phone(self):
    user_phone = str(self.cleaned_data['phone'])
    if len(user_phone) < 9: # The phone number should have  9 or 10 digits.
      raise forms.ValidationError(_('Invalid Phone Number: %(value)s'),
        params={'value': user_phone},)
    return user_phone

