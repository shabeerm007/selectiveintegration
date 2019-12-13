from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django import forms


class SignupForm(UserCreationForm):
	class Meta:
		model = User
		fields =['username','first_name','last_name','email']
	def clean_email(self):
		user_email = self.cleaned_data['email']
		if User.objects.filter(email=user_email): #Check if the email already exists.
			raise forms.ValidationError(_('email already exists'), code='duplicate_email')
		return user_email