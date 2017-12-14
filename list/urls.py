from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.item_list, name='item_list'),
	url(r'^post/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
]