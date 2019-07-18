from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
import requests
import base64
import simplejson as json
import sys, os
from django.conf import settings
import datetime
import uuid
from miniapp.structure import Structure

from .models import Operation, DetailOperation
from product.models import Product

from .serializers import OperationSerializer, DetailOperationSerializer

class OperationDataViewSet(viewsets.ModelViewSet):
	model = Operation
	queryset = model.objects.all()
	serializer_class = OperationSerializer
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
			queryset = super(OperationDataViewSet, self).get_queryset()
			idempotency_token = self.request.query_params.get('idempotency_token', None)
			token = self.request.query_params.get('token', None)
			user = self.request.query_params.get('user', None)
			status_payment_request = self.request.query_params.get('status', None)
			page = self.request.query_params.get('page', None)

			qset = (~Q (id = 0))
			if (idempotency_token or token or user or status_payment_request):
				if idempotency_token:
					qset = qset & (Q(idempotency_token = idempotency_token))
				if token:
					qset = qset & (Q(token = token))
				if user:
					qset = qset & (Q(user = user))
				if status:
					qset = qset & (Q(status = status_payment_request))

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
			reply = Structure.error500()
			return Response(reply, status=status.HTTP_400_BAD_REQUEST)

	def create(self, request, *args, **kwargs):
		if request.method == 'POST':
			try:
				serializer = self.serializer_class(data=request.data,
					context={'request': request})

				if serializer.is_valid():
					serializer.save(user_id=request.user.id,
						user_ip_address=request.environ['REMOTE_ADDR'])

					reply = Structure.success(
						'La operacion ha sido registrada exitosamente.',
						serializer.data)
					
					return Response(reply,status=status.HTTP_201_CREATED)

				else:
					reply = Structure.error(serializer.errors)
					return Response(reply, status=status.HTTP_400_BAD_REQUEST)
			except Exception as e:
				reply = Structure.error500()
				return Response(reply, status=status.HTTP_400_BAD_REQUEST)

	def destroy(self,request,*args,**kwargs):
		if request.method == 'DELETE':			
			try:
				instance = self.get_object()
				self.perform_destroy(instance)
				serializer = self.get_serializer(instance)
				reply = Structure.success(
					'La operacion ha sido eliminada exitosamente.',
					serializer.data)
				return Response(reply, status=status.HTTP_204_NO_CONTENT)
			except Exception as e:
				reply=Structure.error500()				
				return Response(reply, status=status.HTTP_400_BAD_REQUEST)

	@transaction.atomic
	@action(methods=['POST'],detail=False, url_path='create-payment-request',\
	url_name='operation.create-payment-request')
	def createPaymentRequest(self, request,*args,**kwargs):
		try:
			sid = transaction.savepoint()
			# Se espera recibir por POST un array de json que contenga
			# los id de los productos a comprar y su respectiva cantidad
			# [{id:xx, quantity: yy}, {id:xx1, quantity: yy1}, ....]
			data = request.POST.get('data',None)
			currentUserId = request.POST.get('user', request.user.id)
			if data:
				arrayProducts = []
				purchase_items = []
				array = data.split('},')
				idtoken = uuid.uuid1()
				operation = Operation(
					date_operation = datetime.datetime.now(),
					idempotency_token = str(idtoken),
					user_id = currentUserId,
					user_ip_address = request.environ['REMOTE_ADDR'])
				operation.save()

				for element in array:
					stringElement = element.replace('[','').replace(']','')
					stringElement = stringElement + '}' if stringElement[-1] != '}' else stringElement
					arrayProducts.append(json.loads(stringElement))

				

				for product in arrayProducts:
					detailOperation = DetailOperation(
						operation_id = operation.id,
						product_id = product['id'],
						quantity  = product['quantity'])
					detailOperation.save()
					productObj = Product.objects.get(id=product['id'])
					jsonString = '{"name":"' + productObj.name +\
					 '","value":"' + str(int(float(product['quantity']) * productObj.price)) + '"}'
					purchase_items.append(json.loads(jsonString))

				# configuro la fecha y hora de expiracion a 12 horas despues de la creacion
				# de la petición. Le habia colocado 1 hora, pero no conozco la zona horaria
				# que esta manejando el servidor que despliega el API de TPAGA	
				expires_at = operation.date_operation + datetime.timedelta(hours=12)
					
				data = {
						"cost": str(int(operation.subtotal)),
						"purchase_details_url": settings.IP_SERVER + 'admin',
						"voucher_url": settings.IP_SERVER +  \
						'admin/operation/operation/' + str(operation.id) + '/change/',
						"idempotency_token": str(operation.idempotency_token),
						"order_id": str(operation.id),
						"terminal_id": "sede virtual principal",
						"purchase_description": "compra en linea - comercio electronico",
						"purchase_items": purchase_items,
						"user_ip_address": operation.user_ip_address,
						"expires_at": expires_at.isoformat()
						}
					
				c = settings.USER_TPAGA + ':' + settings.CLAVE_TPAGA
				credentials = base64.b64encode(c.encode())
				headers = {
						'Authorization': 'Basic ' + credentials.decode('UTF-8'),
						'Cache-Control': "no-cache",
						'Content-Type': "application/json"
						}

				
				result = requests.post('https://stag.wallet.tpaga.co/merchants/api/v1/payment_requests/create',
					data = json.dumps(data),
					headers = headers)
				#import pdb; pdb.set_trace()	
				operation.token = result.json()['token']
				operation.status = settings.CREATED
				operation.save()
				transaction.savepoint_commit(sid)
				reply = Structure.success(
					'Registro creado correctamente', result.json())
			else:
				reply = Structure.warning(
					'No se recibieron los parametros esperados', None)

			response = Response(reply) 
			return response

		except Exception as e:
			transaction.savepoint_rollback(sid)
			reply = Structure.error500()				
			return Response(reply, status=status.HTTP_400_BAD_REQUEST)	

	@action(methods=['GET'],detail=False, url_path='get-status-payment-request',\
	url_name='operation.get-status-payment-request')
	def createPaymentRequest(self, request,*args,**kwargs):
		try:
			token = request.GET.get('token',None)
			if token:
				c = settings.USER_TPAGA + ':' + settings.CLAVE_TPAGA
				credentials = base64.b64encode(c.encode())
				headers = {
					'Authorization': 'Basic ' + credentials.decode('UTF-8'),
					'Cache-Control': "no-cache",
					'Content-Type': "application/json"
					}
				result = requests.get('https://stag.wallet.tpaga.co/merchants/api/v1/payment_requests/' + \
					token + '/info',headers = headers)

				reply = Structure.success('Resultado satistactorio',
					result.json())
			else:
				reply = Structure.warning('No se encontro en la peticion el parametro token',None)				

			response = Response(reply) 
			return response

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(e, exc_type, fname, exc_tb.tb_lineno)

			reply = Structure.error500()				
			return Response(reply, status=status.HTTP_400_BAD_REQUEST)				


class DetailOperationDataViewSet(viewsets.ModelViewSet):
	model = DetailOperation
	queryset = model.objects.all()
	serializer_class = DetailOperationSerializer
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
			queryset = super(DetailOperationDataViewSet, self).get_queryset()
			idempotency_token = self.request.query_params.get('idempotency_token', None)
			token = self.request.query_params.get('token', None)
			page = self.request.query_params.get('page', None)

			qset = (~Q (id = 0))
			if (idempotency_token or token):
				if idempotency_token:
					qset = qset & (Q(operation__idempotency_token = idempotency_token))
				if token:
					qset = qset & (Q(operation__token = token))

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
			reply = Structure.error500()
			return Response(reply, status=status.HTTP_400_BAD_REQUEST)