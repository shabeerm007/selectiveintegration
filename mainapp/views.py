from django.shortcuts import  render,redirect
from .models import Maths, GeneralA
from qbankapp.models_english import English
from django.views.generic import TemplateView
from .forms import ExamForm, ContactForm
from django.core.mail import send_mail
from django.core import serializers
from random import randint
import time

Maths_db_count = Maths.objects.count() 	# total number of Maths questions in the database
exam_page = 'exam.html'
resultpage = 'result.html'
contactpage = 'contact.html'
emailsentpage = 'emailsent.html'
MATHS_EXAM_TIME =40*60 					# 40 minutes

class TestPaperView(TemplateView):

	@staticmethod
	def render_the_question(request):

		qnum, qelem = TestPaperView.get_question(request)

		#render the choices using the form class
		options = [ ('A', qelem.ch1),
                        ('B', qelem.ch2),
                        ('C', qelem.ch3),
                        ('D', qelem.ch4),
                        ]

    	#If the user is going back to the previous question show the old selection else render a unintialized form.
		form = 	ExamForm(choices = options, initial ={'selectedchoice': request.session['student_answer'][str(request.session['qnum'])]}) \
				if request.session['student_answer'].get(str(request.session['qnum']),0) else \
				ExamForm(choices = options)
		
		
		qstring = f"{qnum}.	{qelem.que}" 			#qstring = Question number + Question
		form_data = {'question' : qstring, 
					'form':form,
					'time':request.session['time_left'],
					}
		return render(request,exam_page, form_data)

	@staticmethod
	def get_question(request):
		'''	Test paper question object is stored are json object.
			Run the desrialiser and retrieve the question record '''
		qnum = request.session['qnum']
		json_record  = request.session['test_paper_q_list'][str(qnum)]

		json_deserialized = [record for record in serializers.deserialize("json", json_record) ]
		'''	deserializer returns a DeserializedObject which is an iterable. In our case there is only one record in it and
			DeserializedObject.object will return the  record.'''
		qelem = json_deserialized[0].object
		return (qnum, qelem)

	def store_answer(self,request,answer):
		qnum = request.session['qnum']
		request.session['student_answer'][qnum] = answer


	@staticmethod
	def get_result(request):
		result = 0

		#Retrive the list of Math object from the deserializedObject list
		question_list = map((lambda serializedobj:
							[rec for rec in serializers.deserialize("json", serializedobj)][0].object),
							 request.session['test_paper_q_list'].values()
							 )
		for question,student_selction in zip(question_list, \
											request.session['student_answer'].values()):
			if question.ans == student_selction:
				result +=1
		return result

	def get(self,request):
		''' Initialize  session variables.
			1. 'test_paper_q_list' with a total of request.session['max_question'] random unique questions from the database.
				Each record is stored in serialized json format.
			2. 'student_answer'  captures the coice selected by the student
			3. 'qnum' will hold the next question number to be rendered
			4. 'max_question' indicates the maximum number of questions in the current test
			5. 'time_left' indicates the remaning time to complete the exam'''

		request.session['test_paper_q_list'], request.session['student_answer'] = {}, {}
		request.session['qnum'] = 1 #Start Question number
		request.session['max_question'] = 20
		
		
		request.session['time_left']= MATHS_EXAM_TIME
		request.session['start_time'] = time.time()

		if request.GET['test'] == 'trial':
			request.session['max_question'] = 20
			maths_obj_list = Maths.objects.all()[0:20]

			for key,record in enumerate(maths_obj_list,start=1):
				json_record  = serializers.serialize("json", [record])
				request.session['test_paper_q_list'].setdefault(str(key), json_record)
			return self.render_the_question(request)

		if not request.user.is_authenticated:
			#If user is not logged in prevent user from taking the actual test.
			return redirect('/accounts/login')

		random_list_of_questions = set()
		while (len(random_list_of_questions)<request.session['max_question']):
			#Get request.session['max_question'] random numbers between zero and total questions in the database
			random_list_of_questions.add(randint(0,Maths_db_count-1))

		for key,record in enumerate(random_list_of_questions,start=1):
			'''prepare the test paper question list for each exam session. Store in json format'''
			json_record = serializers.serialize("json", Maths.objects.all()[record:record +1])
			request.session['test_paper_q_list'].setdefault(str(key), json_record)

		return self.render_the_question(request)


	def post(self,request):

		#update the time elapsed.
		time_left = round(MATHS_EXAM_TIME - (time.time()-request.session['start_time']))	
		request.session['time_left'] = time_left if time_left > 0 else 0

		

		#validate the submitted form
		form = ExamForm(request.POST)
		if form.is_valid():
			#Retrieve the submitted data from form.clean_data and store it in the session variable.
			request.session['student_answer'][request.session['qnum']] = form.cleaned_data['selectedchoice']
			request.session['qnum'] += 	1 if int(request.POST['next']) else \
										-1 if int(request.session['qnum']) > 1 else 0

		if request.session['qnum'] > request.session['max_question'] or request.session['time_left'] ==0:
			return redirect('/result')

		return self.render_the_question(request)


# Create your views here.
def resultview(request,*args, **kwargs):

	score = TestPaperView.get_result(request)
	#We reach here at the end of the exam. Reset the timer to zero if we are here before the timer expires. 
	request.session['time_left']= 0 
	return render (request,resultpage,
                    {'score' : score,
                        'total_marks': request.session['max_question']})


# Create your views here.
def home_view(request,*args, **kwargs):
	print("{}  : {}".format(request, request.user))
	strng = "<H1> Main page of Trilane technologes </H1>"
	return render(request,"home.html")

def test_view(request,*args, **kwargs):
	print("{}  : {}".format(request, request.user))
	strng = "<H1> Main page of Trilane technologes </H1>"
	return render(request,"tests.html")


class ContactView(TemplateView):

	def get(self,request):
		form = ContactForm()
		return render(request,contactpage, {'form':form})

	def post(self,request):
		form = ContactForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data['name']
			user_email = form.cleaned_data['email']
			user_phone = form.cleaned_data['phone']
			user_sub = form.cleaned_data['subject']
			user_message = form.cleaned_data['message']
			email_body = f'''\nname		: {user_name}  \nEmail_id	: {user_email}\nphone		: {user_phone}
							\n-----Message-------- \n{user_message}\n'''
			selective_email = 'selectivetestsmail@gmail.com'
			send_mail(user_sub,email_body,selective_email,[selective_email,])
			return render(request,emailsentpage)

		#Form has errors. Display the form again.	
		return render(request,contactpage, {'form':form})


