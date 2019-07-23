function ProductViewModel(argument) {
	var self=this;
	self.list=ko.observableArray([]);
	self.url=path_principal+'/api/product/';
	self.filter=ko.observable('');
	self.message=ko.observable('');

	self.getData = function (page) {
        if (page > 0) {
            self.filter($('#query').val());
            path = self.url + '?format=json&page=' + page;
            parameter = {
                query: self.filter()
            };
            RequestGet(function(datos, estado, mensage) {
            	//alert(datos.data);
                if (datos.data != null && datos.data.length > 0) {
                    self.message('');
                    self.list(datos.data);
                } else {
                    self.list([]);
                    self.message(mensajeNoFound); //mensaje not found se encuentra el el archivo call-back.js
                }
                self.llenar_paginacion(datos, page);
                cerrarLoading();
            }, path, parameter,undefined,false);
        }
	}

    self.paginacion = {
        pagina_actual: ko.observable(1),
        total: ko.observable(0),
        maxPaginas: ko.observable(5),
        directiones: ko.observable(true),
        limite: ko.observable(true),
        cantidad_por_paginas: ko.observable(0),
        text: {
            first: ko.observable('Inicio'),
            last: ko.observable('Fin'),
            back: ko.observable('<'),
            forward: ko.observable('>')
        }
    }

    //Funcion para crear la paginacion
    self.llenar_paginacion = function (data,page) {
		self.paginacion.pagina_actual(page);
		self.paginacion.total(data.count);
		self.paginacion.cantidad_por_paginas(resultadosPorPagina);

    }

    self.paginacion.pagina_actual.subscribe(function (page) {
        if (self.buscado_rapido()) {
            self.consultar(page);
          }else{
            self.consultar_por_filtros(page);
          }       
    });

    self.createPaymentRequest = function (){
    	var order=[];
        $('.order').each(function(){
        	var element = this;
        	if (element.value > 0){
	        	order.push(JSON.parse('{\"id\":\"'+element.id+'\",\"quantity\":\"'+element.value+'\"}'));
        	}
        });
        if (order.length == 0){
        	$("#message").show();
        }else{
        	$("#message").hide();
        	path = path_principal + "/api/operation/create-payment-request/"
        	parameter = {data: order}
        	var request = {
        		callback:function(datos, estado, mensaje){
        			if (estado == 'success'){
        				$("#message-error").hide();
        				window.location.href = datos.tpaga_payment_url
        			}else{
        				$("#message-error").show();
        			}
        		},
        		url:path,
        		parametros:parameter
        	};
        	Request(request);
        }
        
    }
}

var product = new ProductViewModel();
ko.applyBindings(product);