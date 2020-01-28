from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models_generalability import GeneralA

class CreateGeneralA(CreateView):
	model = GeneralA
	fields = '__all__'

class UpdateGeneralA(UpdateView):
	model = GeneralA
	fields = '__all__'

class DetailGeneralA(DetailView):
	model = GeneralA
	fields = '__all__'

class ListGeneralA(ListView):
	model = GeneralA
	fields = '__all__'
	ordering = ["-pk"]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
