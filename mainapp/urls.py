from django.urls import path
from mainapp.views import (home_view,
							test_view,
							ContactView,
							TestPaperView,
							resultview
							)

urlpatterns = [
	path('',home_view,name='home'),
	path('tests',test_view,name='tests'),
	path('contact',ContactView.as_view(),name='contact'),
	path('exam', TestPaperView.as_view(), name='exam'),
    path('result', resultview, name='result'),
]
