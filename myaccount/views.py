from django.shortcuts import render,redirect
from .forms import SignupForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import  UpdateView
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text


signupform = 'myaccounts/signupform.html'
activationlink = 'myaccounts/activationlink.html'
activationpage = 'myaccounts/activationpage.html'
invalidpage = 'myaccounts/invalidpage.html'

account_activation_token = PasswordResetTokenGenerator()

def make_activation_message(request,user):

	current_site =  get_current_site(request)
	token = account_activation_token.make_token(user)
	
	email_message = render_to_string(activationlink,\
		{	'user' 	:user,
			'domain':current_site.domain,
			'uid'	:urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
			'token'	:token
		}
	)
	return email_message

class SignUpView(TemplateView):

	def get(self,request):
		form = SignupForm()
		return render(request,signupform, {'form':form})

	def post(self,request):
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.is_active = False  #Keep the user inactive till the email is confirmed
			user.save()
			subject = 'Activate your Selective account'
			to_email = form.cleaned_data['email']
			from_email = 'selectivetestsmail@gmail.com'
			email_body = make_activation_message(request,user)
			
			user.email_user(subject=subject,\
							message=email_body)
			return render(request,activationpage)

		#Form has errors. Display the form again.	
		return render(request,signupform, {'form':form})


#Activate the user when signing in the first time.
def useractivateview(request, uidb64, token):

	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)

	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		return redirect('/accounts/login/')
	else:
		return render(request,invalidpage)



'''
class StudentPchange(LoginRequiredMixin,auth_views.PasswordChangeView):
	pass

class StudentPchangeDone(auth_views.PasswordChangeDoneView):
	pass

class StudentLogin(auth_views.LoginView):
	pass

class StudentLogout(auth_views.LogoutView):
	pass


class StudentUpdate(UpdateView):
	pass
'''