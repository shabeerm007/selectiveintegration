
from django import forms
from mainapp.models import Question


class TestForm(forms.Form):

    def __init__(self, *args, **kwargs):
        print("kwargs {}".format(kwargs))
        q_num = kwargs.pop('question_num')
        nextbool = kwargs.pop('nextb')
        
        super(TestForm, self).__init__(*args, **kwargs)
        obj =  Question.objects.get(id=q_num)
        ANS_CHOICE = [
          ('a',obj.ch1),
          ('b',obj.ch2),
          ('c',obj.ch3),
          ('d',obj.ch4),
          ]
        self.fields[f'Que_{q_num}'] = forms.CharField(label='',widget=forms.RadioSelect(choices=ANS_CHOICE),required=nextbool)
