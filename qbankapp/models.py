from django.db import models
from django.urls import reverse


class QContext(models.Model):
	slug 	= models.SlugField(max_length=50, unique=True) 
	text 	= models.TextField(max_length=5*1024, null=True, blank=True)
	image 	= models.ImageField(upload_to='qbank/', null=True, blank=True) 

	def get_absolute_url(self):
		return reverse('detail-qcontext',kwargs={'slug':self.slug})
		
	def __str__(self):
		return self.slug

	def to_dict(self):
		return {'qcslug'	:self.slug,
				'qctext'	:self.text,
				'qcimage'	:self.image.path if (self.image) else None
				}