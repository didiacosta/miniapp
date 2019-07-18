from django.db import models
from simple_history.models import HistoricalRecords
import os
# Create your models here.

from product.models import Product
from usuario.models import User

class Operation(models.Model):
	date_operation = models.DateTimeField(null=True)
	user = models.ForeignKey(User,
		related_name='fk_operation_user',
		on_delete=models.PROTECT)
	idempotency_token = models.CharField(max_length=200, null=True, blank=True)
	token = models.CharField(max_length=200, null=True, blank=True)
	status = models.CharField(max_length=200, default='provisioned')
	user_ip_address = models.CharField(max_length=200,null=True, blank=True)
	history = HistoricalRecords()

	@property
	def _history_user(self):
		return self.changed_by

	@property
	def subtotal(self):
		subtotal = 0
		details = DetailOperation.objects.filter(
			operation=self).values('product__price','quantity')
		for detail in details:
			subtotal = subtotal + (detail['product__price'] * detail['quantity'])
		return subtotal
	

	@_history_user.setter
	def _history_user(self, value):
		self.changed_by = value
	
	def __str__(self):
		return self.user.email + ' - ' + \
		self.date_operation.strftime('%Y-%m-%d %H:%M')

	# def save(self, *args, **kwargs):
	# 	self.date_operation = datetime.datetime.now()
	# 	self.idempotency_token=uuid.uuid1()
	# 	super(Operation, self).save(*args, **kwargs)


class DetailOperation(models.Model):
	operation = models.ForeignKey(Operation,
		related_name='fk_operation_detail',
		on_delete=models.PROTECT)
	product = models.ForeignKey(Product,
		related_name='fk_operation_product',
		on_delete=models.PROTECT)
	quantity = models.IntegerField()

	class Meta:
		unique_together = (("operation","product"),)

	@property
	def _history_user(self):
		return self.changed_by	

	@_history_user.setter
	def _history_user(self, value):
		self.changed_by = value
	
	def __str__(self):
		return self.operation.date_operation.strftime('%Y-%m-%d %H:%M') + ' - ' + \
		self.product.name + ' - (' + str(self.quantity) + ')'

