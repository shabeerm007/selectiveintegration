from django.urls import path
from mainapp.views import *
from mainapp.tests import unittest

urlpatterns = [
	path('',home_view,name='home'),
	path('tests',test_view,name='tests'),
	path('contact',ContactView.as_view(),name='contact'),
	path('exam', ExamView.as_view(), name='exam'),
    path('result', resultview, name='result'),
	path('unittest', unittest, name='unittest'), #activate to pupulate the database.
]
