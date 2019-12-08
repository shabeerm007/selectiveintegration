from django.urls import path
from mainapp.views import *
from mainapp.tests import unittest

urlpatterns = [
	path('',home_view,name='home'),
	path('tests',test_view,name='testpage'),
	path('contact',contact_view,name='contactpage'),
	path('exam', ExamView.as_view(), name='examview'),
        path('result', resultview, name='result'),
        #path('exam', TestView.as_view(), name='examview'),
	#path('unittest', unittest, name='unittest'),
]
