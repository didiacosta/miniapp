from rest_framework import serializers

from .models import Product
from type.models import Type
from type.serializers import TypeSerializerLite

class ProductSerializer(serializers.ModelSerializer):
	typeProduct = TypeSerializerLite(read_only=True)
	typeProduct_id = serializers.PrimaryKeyRelatedField(write_only=True,
		queryset = Type.objects.all())

	class Meta:
		model = Product
		fields = ('id', 'typeProduct','typeProduct_id','name',
			'image','price','sold_out','image_url_absolute')

class ProductSerializerLite(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('id','name','price',)

