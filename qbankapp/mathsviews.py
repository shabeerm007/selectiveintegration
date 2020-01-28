from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models_maths import Maths

class CreateMaths(CreateView):
	model = Maths
	fields = '__all__'

class UpdateMaths(UpdateView):
	model = Maths
	fields = '__all__'

class DetailMaths(DetailView):
	model = Maths
	fields = '__all__'


class ListMaths(ListView):
	model = Maths
	fields = '__all__'
	ordering = ["-pk"]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
