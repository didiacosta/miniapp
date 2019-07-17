from django.contrib import admin
from .models import Product 
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
class AdminProduct(SimpleHistoryAdmin):
	list_display=('id','product_type','image_url','name','price',)
	search_fields= ('name',)
	history_list_display = ("status",)

admin.site.register(Product,AdminProduct)
