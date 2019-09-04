from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.views.generic import TemplateView
from .forms import TestForm


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


MAX_QUESTION = 5

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

		if TestView.index > MAX_QUESTION:
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

		if TestView.index > MAX_QUESTION:
				#if test completed, calculate the student mark and return
				secured_marks = TestView.exam_obj.result()
				return render(request, self.template_result, 
					{'secured_marks' : secured_marks, 'total_marks': MAX_QUESTION})

		#Store the Previous questions Answer in exam obj
		TestView.exam_obj.answer_sheet(TestView.index, request.POST[q_str])


		form = TestForm(request.POST or None, question_num= TestView.index, nextb = False)

		return render(request, self.template_test, {'form':form, 'q': self.get_question() })
