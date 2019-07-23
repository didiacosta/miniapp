from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('home/',views.index_view, name='usuario.index'),
	path('logout/',views.logout_view, name='usuario.logout'),
	path('login/',views.login_view, name='usuario.login'),

]