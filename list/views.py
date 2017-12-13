from django.shortcuts import render
from django.utils import timezone
from .models import ListItem

# Create your views here.

def item_list(request):
	items = ListItem.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'list/item_list.html', {'items': items})