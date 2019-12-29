from django.urls import path,include
from .views import (
	CreateBkpFile,
	CreateDbMaths,
	CreateDbEnglish,
	CreateDbGeneralA,
	ListDbMaths,
	ListDbEnglish,
	ListDbGeneralA,
	UpdateDbMaths,
	UpdateDbEnglish,
	DeleteALLRecordsMaths,
	UpdateDbGeneralA,
	FillQbank
)

urlpatterns = [
    path('fillqbank',FillQbank.as_view(),name='fillqbank'),
    path('create/maths',CreateDbMaths.as_view(),name='create-maths'),
    path('create/english',CreateDbEnglish.as_view(),name='create-english'),
    path('create/generala',CreateDbGeneralA.as_view(),name='create-generala'),
    path('list/maths',ListDbMaths.as_view(),name='list-maths'),
    path('list/english',ListDbEnglish.as_view(),name='list-eng'),
    path('list/generalability',ListDbGeneralA.as_view(),name='list-ga'),
    path('update/maths/<int:pk>',UpdateDbMaths.as_view(),name='update-maths'),
    path('update/english/<int:pk>',UpdateDbEnglish.as_view(),name='update-eng'),
    path('update/generalability/<int:pk>',UpdateDbGeneralA.as_view(),name='update-ga'),
    #path('delete/maths',DeleteALLRecordsMaths.as_view(),name='delete-maths'),
    path('makebackup',CreateBkpFile.as_view(),name='mkbkp'),
]
