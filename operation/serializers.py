from rest_framework import serializers

from .models import Operation, DetailOperation
from usuario.models import User
from product.models import Product

from usuario.serializers import UserSerializerLite
from product.serializers import ProductSerializerLite

class OperationSerializer(serializers.ModelSerializer):
	user = UserSerializerLite(read_only=True)
	user_id = serializers.PrimaryKeyRelatedField(write_only=True,
		queryset = User.objects.all())
    
	class Meta:
		model = Operation
		fields = ('id', 'date_operation','user','user_id',
			'idempotency_token','token','status','user_ip_address',)

class DetailOperationSerializer(serializers.ModelSerializer):
	operation = OperationSerializer(read_only=True)
	operation_id = serializers.PrimaryKeyRelatedField(write_only=True,
		queryset = Operation.objects.all())
	product = ProductSerializerLite(read_only=True)
	product_id = serializers.PrimaryKeyRelatedField(write_only=True,
		queryset = Product.objects.all())

	class Meta:
		model = DetailOperation
		fields = ('id', 'operation','operation_id',
		'product','product_id','quantity')
