from django.shortcuts import *
from django.http import HttpResponse
from .models import *
from django.views.generic import TemplateView
from .forms import *


MAX_QUESTION = 3

# Create your views here.
def resultview(request,*args, **kwargs):

	if request.session['qnum'] > request.session['qset'][1]:
            return render (request,'result.html',
                    {'score' : request.session['score'],
                        'total_marks': MAX_QUESTION})
	return render(request,"result.html")


class ExamView(TemplateView):
	exampage = 'exam.html'
	resultpage = 'result.html'

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
		return render(request,ExamView.exampage, form_data)

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
			return redirect('http://www.selectivetests.gq/result')

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


def contact_view(request,*args, **kwargs):
	print("{}  : {}".format(request, request.user))
	strng = "<H1> Main page of Trilane technologes </H1>"
	#return HttpResponse(strng)
	return render(request,"contact.html")



class Exam:

	def __init__(self):
		self.selection ={}
		self.marks = 0

	def answer_sheet(self, question_num, choice):
		self.selection [question_num]= choice

	def result(self):
		self.marks = 0

		for q_num,selected_ans in self.selection.items():
			obj =  Question.objects.get(id=q_num)
			if obj.ans == selected_ans:
				self.marks +=1

		return self.marks
	def display_workout(self):
		pass


class TestView(TemplateView):

	#template_test = "exam.html"			#Testing page
	#template_result = "result.html"		#Result page
	index = 1							#Question number
	exam_obj = Exam()					#Exam object stores the answersheet, calculates results, displays work sheets

	def __init__(self):
		self.template_test = 'exam.html'
		self.template_result = 'result.html'
		self.action = True #True for next question and False for previous question
		self.obj =  Question.objects.get(id=TestView.index)

	def get_question(self):
		self.obj =  Question.objects.get(id=TestView.index)
		question = f'{TestView.index}. {self.obj.que}'
		return question


	def get(self, request):
		print(f"\nrequest.GET : {request.GET}")

		if TestView.index >= MAX_QUESTION:
			#If test completed, calculate the student mark and return
			secured_marks = TestView.exam_obj.result()
			return render(request, self.template_result,
				{'secured_marks' : secured_marks, 'total_marks': MAX_QUESTION})

		form = TestForm(question_num= TestView.index, nextb = self.action)
		return render(request, self.template_test, {'form':form, 'q': self.get_question() } )

	def post(self, request):
		print(f"\nrequest.POST : {request.POST}")


		#Get the question number string in the POST message
		q_str = f'Que_{TestView.index}'
		
		
		if request.POST['action'] == 'NEXT':
			#Go  to the next question
			if q_str not in request.POST:
				form = TestForm(request.POST or None, question_num= TestView.index, nextb = True)
				return render(request, self.template_test, {'form':form, 'q': self.get_question() })
						#Display the next question
			TestView.index += 1
			self.action = True #unused

		elif request.POST['action'] == 'PREV':
			#Go back to the previous question
			if TestView.index > 1:
				#Display the previous question. If in question 1 keep displaying the same question
				TestView.index -= 1
				self.action = False #unused
			form = TestForm(request.POST or None, question_num= TestView.index, nextb = False)
			return render(request, self.template_test, {'form':form, 'q': self.get_question() })

		if TestView.index >= MAX_QUESTION:
				#if test completed, calculate the student mark and return
				secured_marks = TestView.exam_obj.result()
				return render(request, self.template_result, 
					{'secured_marks' : secured_marks, 'total_marks': MAX_QUESTION})

		#Store the Previous questions Answer in exam obj
		TestView.exam_obj.answer_sheet(TestView.index-1, request.POST[q_str])


		form = TestForm(request.POST or None, question_num= TestView.index, nextb = False)

		return render(request, self.template_test, {'form':form, 'q': self.get_question() })
