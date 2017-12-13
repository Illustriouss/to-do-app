from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.item_list, name='item_list'),
]