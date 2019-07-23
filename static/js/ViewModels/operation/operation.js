function OperationViewModel(argument) {
	var self=this;
	self.list=ko.observableArray([]);
	self.url=path_principal+'/api/operation/';
	self.filter=ko.observable('');
	self.message=ko.observable('');

	self.getData = function (id) {
        if (id > 0) {
        	self.filter(id);
            path = self.url + 'get-status-payment-request?format=json&page=1';
            parameter = {
                id: self.filter()
            };
            RequestGet(function(datos, estado, mensage) {
                if (datos != null) {
            		$("#status").val(datos.status);                	
                    self.message('');
                    self.list(datos.purchase_items);
                } else {
                    self.list([]);
                    self.message(mensajeNoFound); 
                }
                cerrarLoading();
            }, path, parameter,undefined,false);
        }
	}

}
var operation = new OperationViewModel();
ko.applyBindings(operation);