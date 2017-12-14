from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import ListItem

def item_list(request):
	items = ListItem.objects.filter(published_date__lte=timezone.now()).order_by('end_date')
	return render(request, 'list/item_list.html', {'items': items})

def item_detail(request, pk):
	item = get_object_or_404(ListItem, pk=pk)
	return render(request, 'list/item_detail.html', {'item': item})