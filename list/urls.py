from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.new, name='new'),
	url(r'^list/(?P<pk>\d+)/(?P<slug>[-\w]+)/$', views.list, name='list'),
	url(r'^post/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
	url(r'^toggle_done/$', views.toggle_done, name='toggle_done'),
	url(r'^add_item/$', views.add_item, name='add_item'),
	url(r'^remove_item/$', views.remove_item, name='remove_item'),
	url(r'^add_list/$', views.add_list, name='add_list'),
	url(r'^remove_list/$', views.remove_list, name='remove_list'),
	url(r'^log_out/$', views.log_out, name='log_out'),
]