from django.urls import path
from .views import (
	CopytoDatabase,
	CopytoFile
)
from .qcontextviews import (
	CreateQContext,
	UpdateQContext, 
	DetailQContext, 
	ListQContext 
	)
from .englishviews import (
	CreateEnglish,
	UpdateEnglish,
	DetailEnglish,
	ListEnglish
	)
from .generalabilityviews import (
	CreateGeneralA,
	UpdateGeneralA,
	DetailGeneralA,
	ListGeneralA
	)
from .mathsviews import (
	CreateMaths,
	UpdateMaths,
	DetailMaths,
	ListMaths
	)

urlpatterns = [
    path('fill',CopytoDatabase.as_view(),name='fill-database'),
    path('createbackup',CopytoFile.as_view(),name='createbackup'),
    #******************************************************#
    path("qcontext/create", CreateQContext.as_view(),name='create-qcontext'),
    path("qcontext/list", ListQContext.as_view(),name='list-qcontext'),
    path("qcontext/<slug:slug>", DetailQContext.as_view(),name='detail-qcontext'),
    path("qcontext/update/<int:pk>", UpdateQContext.as_view(),name='update-qcontext'),
    #******************************************************#
    path("english/create", CreateEnglish.as_view(),name='create-english'),
    path("english/list", ListEnglish.as_view(),name='list-english'),
    path("english/<int:pk>", DetailEnglish.as_view(),name='detail-english'),
    path("english/update/<int:pk>", UpdateEnglish.as_view(),name='update-english'),
    #******************************************************#
    path("generalability/create", CreateGeneralA.as_view(),name='create-generalability'),
    path("generalability/list", ListGeneralA.as_view(),name='list-generalability'),
    path("generalability/<int:pk>", DetailGeneralA.as_view(),name='detail-generalability'),
    path("generalability/update/<int:pk>", UpdateGeneralA.as_view(),name='update-generalability'),
	#******************************************************#
	path("maths/create", CreateMaths.as_view(),name='create-maths'),
    path("maths/list", ListMaths.as_view(),name='list-maths'),
    path("maths/<int:pk>", DetailMaths.as_view(),name='detail-maths'),
    path("maths/update/<int:pk>", UpdateMaths.as_view(),name='update-maths'),
]
