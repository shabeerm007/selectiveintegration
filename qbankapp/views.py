from django.shortcuts import redirect
from django.http.response import HttpResponse,HttpResponseNotFound
from django.views.generic import TemplateView
from django.core.files import File

from .models_generalability import GeneralA
from .models_english import English
from .models_maths import Maths
from .models import QContext

import os
import pandas as pd
import sys
import openpyxl


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bkp_dir = os.path.join(project_dir,'bkpdir')

class CopytoDatabase(TemplateView):
	'''Read the questons from the file and populate the database'''

	@staticmethod
	def save_record(obj,row):

		if isinstance(obj,QContext):
			#This block is to fill the QContext database.
			obj.slug = row[0]
			obj.text = row[1].values[0] if isinstance(row[1].values[0], str) else ""
			if isinstance(row[1].values[1], str):
				#Create the image field if this qcontext has image files.
				print(row[1].values[1], " : Image field : ",  obj.image)
				print(os.path.basename(row[1].values[1]))
				obj.image.save(os.path.basename(row[1].values[1]), File(open(row[1].values[1], 'rb')))
			obj.save()
			return
		#We come here for filling the Question models - English, GeneralA & Maths
		#obj.pk 	= row[0]. Let Postgres manage the pk.
		obj.que 	= row[1].values[0] if row[1].values[0] else "Default Question"
		obj.ch1 	= row[1].values[1]	if row[1].values[1] else "Choice"
		obj.ch2 	= row[1].values[2]	if row[1].values[2] else "Choice"
		obj.ch3 	= row[1].values[3]	if row[1].values[3] else "Choice"
		obj.ch4 	= row[1].values[4]	if row[1].values[4] else "Choice"
		obj.ans   	= row[1].values[5]	if row[1].values[5] else "Answer"
		obj.wor 	= row[1].values[6]	if row[1].values[6] else "Working out"
		obj.valid 	= row[1].values[7]	if row[1].values[7] else False
		
		#Add the Question context if present
		if (isinstance(row[1].values[8],str) and QContext.objects.filter(slug__exact = row[1].values[8]).exists()):
			obj.context = QContext.objects.get(slug__exact = row[1].values[8])
		else:
			obj.context = None
		obj.save()

	def get(self,request):
		#URL - <domain>/fill?filename=Master*.xlsx&subject=maths

		try:
			filename = request.GET['filename']
			file_abs_path = os.path.join(bkp_dir,filename)
			print(filename, request.GET['subject'], sep=' : ')

			if request.GET['subject'] == 'maths':
				sheet_name = 'Maths'
				cls = Maths
			elif request.GET['subject'] == 'english':
				sheet_name = 'English'
				cls = English
			elif request.GET['subject'] == 'generalability':
				sheet_name = 'General Ability'
				cls = GeneralA
			elif request.GET['subject'] == 'qcontext':
				sheet_name = 'Question Context'
				cls=QContext
			else:
				raise sys.Exception("Invalid URL")

			cls.objects.all().delete() #delete all the records
			
			if __debug__ : #set PYTHONOPTIMIZE env to disable debug.
				assert cls.objects.count() == 0, "The data base is not Empty" 
			
			excel_df = pd.read_excel(file_abs_path,index_col=0,sheet_name=sheet_name)
			
			for row in  excel_df.iterrows(): #Iterarate through the dataframe and save it to the DB.
				print(row[0])
				if not row[0]:
					raise ValueError("Question number(index) is zero in the Excel file")
				self.save_record(cls(),row)
			
		except ValueError:
			return HttpResponse("Index is Zero in Excel file. Non-Zero index expected")
		except AssertionError:
			return HttpResponse( '<h1>The Database have Elements. Empty it before filling it.</h1>')
		except :
			print(sys.exc_info())
			return  HttpResponseNotFound( '<h1>Page not found: Invalid url</h1>')

		return redirect(f"/qbank/{request.GET['subject']}/list")

class CopytoFile(TemplateView):
	'''Read the questons from the DB and write to excel'''

	def get(self,request):
		#URL - <domain>/createbackup?filename=bkp1.xlsx&subject=maths
		try:
			filename = request.GET['filename']
			subject	 = request.GET['subject']
			file_abs_path = os.path.join(bkp_dir,filename)
			print(file_abs_path)

			if request.GET['subject'] == 'maths':
				objects_list = Maths.objects.all().order_by('pk')
				sheetname = 'Maths'
			elif request.GET['subject'] == 'english':
				objects_list = English.objects.all().order_by('pk')
				sheetname = 'English'
			elif request.GET['subject'] == 'generalability':
				objects_list = GeneralA.objects.all().order_by('pk')
				sheetname = 'General Ability'
			elif request.GET['subject'] == 'qcontext':
				objects_list = QContext.objects.all().order_by('slug')
				sheetname = 'Question Context'
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
	
		if sheetname == 'Question Context':
			#Create the dataframe for question context model.
			df_list =[row.to_dict() for row in objects_list]
		else:
			#Create the dataframe for question models.
			df_list = list()	
			for row in objects_list:
				d = row.to_dict()
				d.update(row.context.to_dict() if row.context else {}) #Add Question context if present.
				df_list.append(d)

		df = pd.DataFrame.from_records(df_list)
		with pd.ExcelWriter(file_abs_path,mode=write_mode) as writer:
			df.to_excel(writer,sheet_name=sheetname,
				encoding='UTF-8',index=False)

		return HttpResponse(df.to_html())
