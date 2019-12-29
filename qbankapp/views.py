from django.shortcuts import render, redirect
from django.http.response import HttpResponse,HttpResponseNotFound
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView
from mainapp.models import Maths,English,GeneralA
import os
import pandas as pd
import sys
import openpyxl

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bkp_dir = os.path.join(project_dir,'bkpdir')
qlistpage = 'mainapp/question_list.html'

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
				sheetname = 'General Ability'
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


class FillQbank(CreateView):
	'''Read the questons from the file and populate the database'''

	@staticmethod
	def save_record(obj,row):
		obj.pk 		= row[0]
		obj.que 	= row[1].values[0] if row[1].values[0] else "Default Question"
		obj.ch1 	= row[1].values[1]	if row[1].values[1] else "Choice"
		obj.ch2 	= row[1].values[2]	if row[1].values[2] else "Choice"
		obj.ch3 	= row[1].values[3]	if row[1].values[3] else "Choice"
		obj.ch4 	= row[1].values[4]	if row[1].values[4] else "Choice"
		obj.ans   	= row[1].values[5]	if row[1].values[5] else "Answer"
		obj.wor 	= row[1].values[6]	if row[1].values[6] else "Working out"
		obj.valid 	= row[1].values[7]	if row[1].values[7] else False
		obj.save()

	def get(self,request):
		#URL - <domain>/fillqbank?filename=bkp1.xlsx&subject=maths
		try:
			filename = request.GET['filename']
			file_abs_path = os.path.join(bkp_dir,filename)

			if request.GET['subject'] == 'maths':
				sheet_name = 'Maths'
				cls = Maths
			elif request.GET['subject'] == 'english':
				sheet_name = 'English'
				cls = English
			elif request.GET['subject'] == 'generalability':
				sheet_name = 'General Ability'
				cls = English
			else:
				raise sys.Exception("Invalid URL")

			cls.objects.all().delete() #delete all the records
			if __debug__ : #set PYTHONOPTIMIZE env to disable debug.
				assert cls.objects.count() == 0, "The data base is not Empty" 

			excel_df = pd.read_excel(file_abs_path,index_col=0,sheet_name=sheet_name)

			for row in  excel_df.iterrows(): #Iterarate ththrough the dataframe and save it to the DB.
				
				if not row[0]:
					raise ValueError("Question number(index) is zero in the Excel file")
				self.save_record(cls(),row)
			#To DO: Update the postgres sql sequence number.
			#ALTER SEQUENCE mainapp_maths_id_seq RESTART WITH <number>;
		except ValueError:
			return HttpResponse("Index is Zero in Excel file. Non-Zero index expected")
		except AssertionError:
			return HttpResponse( '<h1>The Database have Elements. Empty it before filling it.</h1>')
		except :
			print(sys.exc_info())
			return  HttpResponseNotFound( '<h1>Page not found: Invalid url</h1>')

		return redirect(f"/qbank/list/{request.GET['subject']}")


class DeleteALLRecordsMaths(TemplateView):

	def get(self,request):
		Maths.objects.all().delete()
		return redirect('/qbank/list/maths')

class CreateDbMaths(CreateView):
	model = Maths
	fields = '__all__'

class CreateDbEnglish(CreateView):
	model = English
	fields = '__all__'

class CreateDbGeneralA(CreateView):
	model = GeneralA
	fields = '__all__'

class UpdateDbMaths(UpdateView):
	model = Maths
	fields = '__all__'

class UpdateDbEnglish(UpdateView):
	model = English
	fields = '__all__'

class UpdateDbGeneralA(UpdateView):
	model = GeneralA
	fields = '__all__'

class ListDbMaths(ListView):
	model = Maths
	template_name = qlistpage
	ordering = ["-pk"]
	
	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super().get_context_data(**kwargs)
	    # Update the subject to be displayed in the template
	    context['subject'] = "Maths"
	    return context

class ListDbEnglish(ListView):
	model = English
	template_name = qlistpage
	ordering = ["-pk"]
	
	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super().get_context_data(**kwargs)
	    # Update the subject to be displayed in the template
	    context['subject'] = "English"
	    return context

class ListDbGeneralA(ListView):
	model = GeneralA
	template_name = qlistpage
	ordering = ["-pk"]
	
	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super().get_context_data(**kwargs)
	    # Update the subject to be displayed in the template
	    context['subject'] = "General Ability"
	    return context


