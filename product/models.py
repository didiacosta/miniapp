from django.db import models
from simple_history.models import HistoricalRecords
from django.utils.html import format_html
import cloudinary
import cloudinary.uploader
import cloudinary.api

from cloudinary.models import CloudinaryField
from django.conf import settings

from type.models import Type
# Create your models here.

class Product(models.Model):
	product_type = models.ForeignKey(Type,
		related_name='fk_product_type',
		on_delete=models.PROTECT)
	name = models.CharField(max_length=200)
	image = CloudinaryField('image',null=True)
	price = models.FloatField(default=0)
	sold_out = models.BooleanField(default=False)
	history = HistoricalRecords()

	def image_url(self):
		#return """<img src="%s"> """ % self.image.url
		return format_html('<img src="{}" width="100" height="100"/>'.format(self.image.url))

	image_url.allow_tags = True

	@property
	def image_url_absolute(self):
		return self.image.url	

	@property
	def _history_user(self):
		return self.changed_by

	@_history_user.setter
	def _history_user(self, value):
		self.changed_by = value
	
	def __str__(self):
		return self.name

	class Meta:
		unique_together = (("name",),)

