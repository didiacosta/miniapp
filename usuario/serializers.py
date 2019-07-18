from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import User

class UserSerializer(serializers.ModelSerializer):	
	class Meta:
		model = User
		fields = ('id', 'url', 'email', 'first_name', 'last_name', 'is_superuser', 
			'is_staff', 'is_active',)

class UserSerializerLite(serializers.ModelSerializer):	
	class Meta:
		model = User
		fields = ('id', 'email', 'first_name', 'last_name')
	
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id', 'name', )	