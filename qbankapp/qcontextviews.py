from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import QContext

# Create your views here.
class CreateQContext(CreateView):
	model = QContext
	fields = '__all__'

class UpdateQContext(UpdateView):
	model = QContext
	fields = '__all__'

class DetailQContext(DetailView):
	model = QContext
	fields = '__all__'

class ListQContext(ListView):
	model = QContext
	fields = '__all__'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context