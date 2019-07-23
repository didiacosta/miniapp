from django.shortcuts import render_to_response, render, redirect
from django.urls import reverse
from django.template import RequestContext
# App
from miniapp.structure import Structure

# Django
from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

# Rest_framework
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, permissions, viewsets#routers, serializers
from rest_framework.response import Response

# Oauth2_provider
#from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication#TokenHasScope


# Serializers
from .serializers import UserSerializer
# Models
from .models import User

# ViewSets define the view behavior.
class UsuarioViewSet(viewsets.ModelViewSet):	
	model = User
	# authentication_classes = [OAuth2Authentication]
	# permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
	queryset = User.objects.all()
	serializer_class = UserSerializer
	paginate_by = 50
	nombre_modulo = 'Usuario'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			respuesta=Estructura.success('', serializer.data)
			return Response(respuesta)
		except Exception as e:
			# print e
			respuesta=Estructura.error('No se encontraron registros')
			return Response(respuesta, status=status.HTTP_404_NOT_FOUND)
			
	def list(self, request, *args, **kwargs):
		try:
			queryset = super(UsuarioViewSet, self).get_queryset()
			page = self.request.query_params.get('page', None)
			dato = self.request.query_params.get('dato', None)
			email = self.request.query_params.get('email', None)
			username = self.request.query_params.get('username', None)
			
			qset = (~Q(id=0))

			if dato:					
				qset = qset & (	Q(email__icontains = dato) | 
					   			Q(first_name__icontains = dato) |
					   			Q(last_name__icontains = dato))
			if email:
				qset = qset & Q(email= email)	

			if username:
				qset = qset & Q(email= username)	
			
			queryset = self.model.objects.filter(qset)				
			mensaje = 'No se encontraron registros con los' + \
					' criterios de busqueda ingresados.' if queryset.count()==0 else ''

			if page:
				paginacion = self.paginate_queryset(queryset)

				if paginacion is not None:
					serializer = self.get_serializer(paginacion,many=True)		
					return self.get_paginated_response(Estructura.success(mensaje ,serializer.data))

			serializer = self.get_serializer(queryset,many=True)
			return Response(Estructura.success(mensaje ,serializer.data))

		except Exception as e:
			funciones.toLog(e,self.nombre_modulo)
			respuesta=Estructura.error500()
			return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

	def create(self, request, *args, **kwargs):
		if request.method == 'POST':			
			try:
				serializer = self.serializer_class(data=request.data,context={'request': request})
				
				if serializer.is_valid():
					serializer.save()
					respuesta = Estructura.success('El usuario ha sido guardado exitosamente.',serializer.data)
					return Response(respuesta,status=status.HTTP_201_CREATED)
				else:					
					respuesta=Estructura.error(serializer.errors)
					return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)
			except Exception as e:
				funciones.toLog(e,self.nombre_modulo)
				respuesta = Estructura.error500()				
				return Response(respuesta, status = status.HTTP_400_BAD_REQUEST)

	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':			
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()
				serializer = self.serializer_class(instance, data=request.data, context={'request': request}, partial=partial)
				if serializer.is_valid():
					serializer.save()				
					respuesta=Estructura.success('El usuario ha sido actualizado exitosamente.',serializer.data)
					return Response(respuesta,status=status.HTTP_201_CREATED)
				else:
					respuesta=Estructura.error(serializer.errors)
					return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)
			except Exception as e:
				funciones.toLog(e,self.nombre_modulo)
				respuesta=Estructura.error500()				
				return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)
							
	def destroy(self,request,*args,**kwargs):
		if request.method == 'DELETE':			
			try:
				instance = self.get_object()
				serializer = self.get_serializer(instance)
				self.perform_destroy(instance)
				respuesta=Estructura.success('El usuario ha sido eliminado exitosamente.',serializer.data)
				return Response(respuesta, status=status.HTTP_204_NO_CONTENT)
			except Exception as e:
				funciones.toLog(e,self.nombre_modulo)
				respuesta=Estructura.error500()				
				return Response(respuesta, status=status.HTTP_400_BAD_REQUEST)

def index_view(request):
	return render(request,'usuario/index.html',{})	

def logout_view(request):
	logout(request)
	return redirect(reverse('usuario.index'))

def login_view(request):
	if request.user.is_authenticated:
		return redirect(reverse('usuario.index'))

	message = ''	
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(email = email, password = password)

		if user:
			if user.is_active:
				login(request, user)
				return redirect(reverse('usuario.index'))
			else:
				message = 'Cuenta inactiva'
		else:
			message = 'Nombre de usuario o clave no valido.'
	
	return render(request, 'usuario/index.html', {'message': message})
