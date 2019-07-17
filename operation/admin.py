from django.contrib import admin
from .models import Operation, DetailOperation
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
class AdminOperation(SimpleHistoryAdmin):
	list_display=('id','date_operation','subtotal',
		'status','idempotency_token',
		'token','user_ip_address',)
	list_filter = ('date_operation', 'status',)
	search_fields= ('token',)
	history_list_display = ("status",)

admin.site.register(Operation,AdminOperation)

class AdminDetailOperation(SimpleHistoryAdmin):
	list_display=('id','operation','product','quantity',)
	history_list_display = ("status",)

admin.site.register(DetailOperation,AdminDetailOperation)
