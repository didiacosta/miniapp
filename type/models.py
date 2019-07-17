from django.db import models
from simple_history.models import HistoricalRecords
# Create your models here.

class Type(models.Model):
	name = models.CharField(max_length=200)
	app = models.CharField(max_length = 250)
	color = models.CharField(max_length = 250 , blank=True)
	icon = models.CharField(max_length = 200 , blank=True)
	history = HistoricalRecords()

	@property
	def _history_user(self):
		return self.changed_by

	@_history_user.setter
	def _history_user(self, value):
		self.changed_by = value
	
	def __str__(self):
		return self.app + '.' + self.name
	class Meta:
		unique_together = (("app" , "name" ),)
