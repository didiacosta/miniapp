from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q

from .models import Product

from .serializers import ProductSerializer

from miniapp.structure import Structure

class ProductDataViewSet(viewsets.ModelViewSet):
	model = Product
	queryset = model.objects.all()
	serializer_class = ProductSerializer
	paginate_by = 20

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			reply = Structure.success('', serializer.data)
			return Response(reply)
		except Exception as e:
			reply=Structure.error('No se encontraron registros')
			return Response(reply, status=status.HTTP_404_NOT_FOUND)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(ProductDataViewSet, self).get_queryset()
			query = self.request.query_params.get('query', None)
			page = self.request.query_params.get('page', None)

			qset = (~Q (id = 0))
			if query:
				qset = qset & (Q(name__icontains = query))

			queryset = self.model.objects.filter(qset)
			if page:
				pagination = self.paginate_queryset(queryset)
				if pagination is not None:
					serializer = self.get_serializer(pagination, many=True)
					reply = Structure.success('', serializer.data)
					return self.get_paginated_response(reply)

			serializer = self.get_serializer(queryset,many=True)

			reply = Structure.success('', serializer.data)
			return Response(reply)

		except Exception as e:
			print (e)
			reply = Structure.error500()
			return Response(reply, status=status.HTTP_400_BAD_REQUEST)
