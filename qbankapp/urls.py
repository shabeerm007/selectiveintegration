from django.urls import path,include
from .views import FiletoDatabase, InputQuestion,ListDbMaths,CreateBkpFile,ListDbEnglish,ListDbGeneralA

urlpatterns = [
    path('copytodb',FiletoDatabase.as_view(),name='copytodb'),
    path('inputq',InputQuestion.as_view(),name='inputq'),
    path('list/maths',ListDbMaths.as_view(),name='listmaths'),
    path('list/english',ListDbEnglish.as_view(),name='listenglish'),
    path('list/generalability',ListDbGeneralA.as_view(),name='listgenerala'),
    path('makebackup',CreateBkpFile.as_view(),name='mkbkp'),
]
