from rest_framework import serializers

from .models import Type

class TypeSerializerLite(serializers.ModelSerializer):
	class Meta:
		model = Type
		fields = ('id', 'name',)