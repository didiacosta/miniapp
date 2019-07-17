from django.contrib import admin
from .models import Type
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
class AdminType(SimpleHistoryAdmin):
	list_display=('id','name','app','color','icon',)
	list_filter = ('app', )
	search_fields= ('name',)
	history_list_display = ("status",)

admin.site.register(Type,AdminType)
