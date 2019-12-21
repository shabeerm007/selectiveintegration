from django.shortcuts import *
from django.http import HttpResponse
from .models import Maths,English, GeneralA
from django.views.generic import TemplateView
from .forms import ExamForm, ContactForm
from django.core.mail import send_mail

MAX_QUESTION = 3

exampage = 'exam.html'
resultpage = 'result.html'
contactpage = 'contact.html'
emailsentpage = 'emailsent.html'

# Create your views here.
def resultview(request,*args, **kwargs):

	if request.session['qnum'] > request.session['qset'][1]:
            return render (request,resultpage,
                    {'score' : request.session['score'],
                        'total_marks': MAX_QUESTION})
	return render(request,resultpage)


class ExamView(TemplateView):
	'''
	Use session variable request.session to store the below values.
		1. Current Question number
		2. Dictionary of the question number and correct answer
		3. Dictionary of the question number and user selected answer
		4. Real time Score
		5. qset - start and end question numbers from teh question bank for this test.
	'''

	def renderthequestion(self, request):
		#get the question from the database
		#store the correct choice as well here.
		qelem = Maths.objects.get(id=request.session['qnum'])
		request.session['correct_ans'][request.session['qnum']]  = qelem.ans

		#render the choices using the form class
		options = [ ('choice1', qelem.ch1),
                        ('choice2', qelem.ch2),
                        ('choice3', qelem.ch3),
                        ('choice4', qelem.ch4),
                        ]
		form = ExamForm(choices = options)
		qstring = f"{request.session['qnum']}.	{qelem.que}" #qstring = Question number + Question
		form_data = {'question' : qstring, 'form':form}
		return render(request,exampage, form_data)

	def get(self,request):
		#Initialize the session variables
		startqnum = 1
		endqnum = startqnum+MAX_QUESTION -1

		request.session['qnum'] = startqnum
		request.session['selected_ans'] = {}
		request.session['correct_ans'] = {}
		request.session['score'] =0
		request.session['qset']= (startqnum,endqnum)

		return self.renderthequestion(request)

	def post(self,request):

		#validate the submitted form
		form = ExamForm(request.POST)

		if form.is_valid():
                    print(f"{request.session['correct_ans']} -  {request.session['selected_ans']}")

                    #Retrieve the submitted data from form.clean_data and store it in the session variable.
                    request.session['selected_ans'][request.session['qnum']] = form.cleaned_data['selectedchoice']
                    #Calculate the score on the go. converting request.session['qnum'] to str for indexing to 
                    #request.session['correct_ans'] to avoid key error.
                    if request.session['selected_ans'][request.session['qnum']] == request.session['correct_ans'][str(request.session['qnum'])]:
                        request.session['score'] +=1 
                    request.session['qnum'] +=1

		if request.session['qnum'] > request.session['qset'][1]:
			return redirect('/result')

		return self.renderthequestion(request)


# Create your views here.
def home_view(request,*args, **kwargs):
	print("{}  : {}".format(request, request.user))
	strng = "<H1> Main page of Trilane technologes </H1>"
	#return HttpResponse(strng)
	return render(request,"home.html")

def test_view(request,*args, **kwargs):
	print("{}  : {}".format(request, request.user))
	strng = "<H1> Main page of Trilane technologes </H1>"
	#return HttpResponse(strng)
	return render(request,"tests.html")


class ContactView(TemplateView):

	def get(self,request):
		form = ContactForm()
		#return render(request,contactpage, {'form':form})
		return render(request,'myaccounts/login.html')

	def post(self,request):
		form = ContactForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data['name']
			user_email = form.cleaned_data['email']
			user_phone = form.cleaned_data['phone']
			user_sub = form.cleaned_data['subject']
			user_message = form.cleaned_data['message']
			email_body = f'''\nname  	: {user_name}  \nEmail_id	: {user_email}\nphone 	: {user_phone} 
							\n-----Message-------- \n{user_message}\n'''
			selective_email = 'selectivetestsmail@gmail.com'
			send_mail(user_sub,email_body,selective_email,[selective_email,])
			return render(request,emailsentpage)

		#Form has errors. Display the form again.	
		return render(request,contactpage, {'form':form})


