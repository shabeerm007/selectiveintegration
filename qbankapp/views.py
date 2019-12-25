from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseNotFound
from django.views.generic import TemplateView,ListView
from .forms import MathsForm, EnglishForm, GeneralAForm
from mainapp.models import Maths,English,GeneralA
import os
import pandas as pd
import sys
import openpyxl

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bkp_dir = os.path.join(project_dir,'bkpdir')
qlistpage = 'qbankapp/question_list.html'
qentrypage = 'qbankapp/que_entry_form.html'

class FiletoDatabase(TemplateView):
	'''Read the questons from the file and populate the database'''

	@staticmethod
	def copyexceltodb(obj,row):
		obj.pk 		= row[0]
		obj.que 	=row[1].values[0] if row[1].values[0] else "Default Question"
		obj.ch1 	= row[1].values[1]	if row[1].values[1] else "Choice"
		obj.ch2 	= row[1].values[2]	if row[1].values[2] else "Choice"
		obj.ch3 	= row[1].values[3]	if row[1].values[3] else "Choice"
		obj.ch4 	= row[1].values[4]	if row[1].values[4] else "Choice"
		obj.ans   	= row[1].values[5]	if row[1].values[5] else "Answer"
		obj.wor 	=  row[1].values[6]	if row[1].values[6] else "Working out"
		obj.valid 	= row[1].values[7]	if row[1].values[7] else False
		obj.save()

	def get(self,request):
		'''
		URL - <domain>/copytodb?filename=bkp1.xlsx&subject=maths
		'''
		try:
			filename = request.GET['filename']
			file_abs_path = os.path.join(bkp_dir,filename)
			if request.GET['subject'] == 'maths':
				obj = Maths()
				excel_df = pd.read_excel(file_abs_path,index_col=0,sheet_name='Maths')#include sheet for maths
			elif request.GET['subject'] == 'english':
				obj = English()
				excel_df = pd.read_excel(file_abs_path,index_col=0,sheet_name='English')#include sheet for maths
			elif request.GET['subject'] == 'generalability':
				obj = GeneralA()
				excel_df = pd.read_excel(file_abs_path,index_col=0,sheet_name='Generl Ability')#include sheet for maths
			else:
				raise sys.Exception("Invalid URL")

			for row in  excel_df.iterrows():
				#Iterarate ththrough the dataframe and save it to the DB.
				if not row[0]:
					raise ValueError("Question number(index) is zero in the Excel file")
				self.copyexceltodb(obj,row)		
		except ValueError:
			return HttpResponse("Index is Zero is Excel file. Non-Zero index expected")
		except :
			print(f"{request.GET} --- {sys.exc_info()}")
			return  HttpResponseNotFound( '<h1>Page not found</h1>')
		return HttpResponse(excel_df.to_html())

class CreateBkpFile(TemplateView):
	'''Read the questons from the DB and write to excel'''

	def get(self,request):
		#URL - <domain>/makebackup?filename=bkp1.xlsx&subject=maths
		try:
			filename = request.GET['filename']
			subject	 = request.GET['subject']
			file_abs_path = os.path.join(bkp_dir,filename)
			print(file_abs_path)

			if request.GET['subject'] == 'maths':
				objects_list = Maths.objects.all()
				sheetname = 'Maths'
			elif request.GET['subject'] == 'english':
				objects_list = English.objects.all()
				sheetname = 'English'
			elif request.GET['subject'] == 'generalability':
				objects_list = GeneralA.objects.all()
				sheetname = 'Generl Ability'
			else:
				raise sys.Exception("Invalid URL")
		except:
			print(f"{request.GET} --- {sys.exc_info()}")
			return HttpResponseNotFound( '<h1>Page not found</h1>')


		if os.path.exists(file_abs_path):
			'''
			Panada dataframe will append a new sheet if the file exists.
			Delete the sheet if subject sheet exists already.
			Let Panda create a new file if there is only one sheet and that is the one to be updated.
			'''
			write_mode = 'a'
			workbook =  openpyxl.load_workbook(file_abs_path)
			if sheetname in workbook.get_sheet_names():
				if len(workbook.get_sheet_names()) >1:
					std = workbook.get_sheet_by_name(sheetname)
					workbook.remove_sheet(std)
					workbook.save(file_abs_path)
				else:
					write_mode = 'w' #create a new file
		else:
			write_mode = 'w' #create a new file

		df = pd.DataFrame.from_records(row.to_dict() for row in objects_list)
		with pd.ExcelWriter(file_abs_path,mode=write_mode) as writer:
			df.to_excel(writer,sheet_name=sheetname,
				encoding='UTF-8',index=False)

		return HttpResponse(df.to_html())


class InputQuestion(TemplateView):
	
	@staticmethod
	def getform(subject, param=None):
		form = None
		if subject == 'Maths':
			form = MathsForm(param)
		elif subject == 'English':
			form = EnglishForm(param)
		elif subject == 'General Ability':
			form = GeneralAForm(param)
		return form

	def get(self,request):
		#URL - <domain>/inputq?subject=maths
		try:
			if request.GET['subject'] == 'maths':
				form = MathsForm()
				subject = 'Maths'	
			elif request.GET['subject'] == 'english':
				form = EnglishForm()
				subject = 'English'
			elif request.GET['subject'] == 'generalability':
				form = GeneralAForm()
				subject = 'General Ability'
			else:
				raise sys.Exception("Invalid URL")
		except:
			return HttpResponseNotFound( '<h1>Page not found</h1>')
		context = {'form':form,'sub':subject}
		return render(request, qentrypage, context)

	def post(self,request):
		subject = request.POST['subject']
		form = self.getform(subject,request.POST)

		if form and form.is_valid():
			form.save()
			form = self.getform(subject)
			context= {'form':form,'sub':subject}
		return render(request, qentrypage, context)

class ListDbMaths(ListView):
	Model = Maths
	queryset = Maths.objects.all()
	template_name = qlistpage
	
	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super().get_context_data(**kwargs)
	    # Update the subject to be displayed in the template
	    context['subject'] = "Maths"
	    return context

class ListDbEnglish(ListView):
	Model = English
	queryset = English.objects.all()
	template_name = qlistpage
	
	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super().get_context_data(**kwargs)
	    # Update the subject to be displayed in the template
	    context['subject'] = "English"
	    return context

class ListDbGeneralA(ListView):
	Model = GeneralA
	queryset = GeneralA.objects.all()
	template_name = qlistpage
	
	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super().get_context_data(**kwargs)
	    # Update the subject to be displayed in the template
	    context['subject'] = "General Ability"
	    return context


