from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models_english import English

class CreateEnglish(CreateView):
	model = English
	fields = '__all__'

class UpdateEnglish(UpdateView):
	model = English
	fields = '__all__'

class DetailEnglish(DetailView):
	model = English
	fields = '__all__'


class ListEnglish(ListView):
	model = English
	fields = '__all__'
	ordering = ["-pk"]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context