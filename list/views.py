from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import date
from .models import List
from .models import Item
from .forms import ItemForm
from .forms import ListForm
import json
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.defaultfilters import slugify

from django.contrib.auth import logout

def new(request):

	if request.user.is_authenticated:

		default_list = List.objects.all().filter(owner=request.user)[0]
		slug=default_list.slug
		pk = default_list.pk
		url = 'list/' + str(pk) + '/' + slug
		return redirect(url)

	return render(request, 'list/new.html')

def list(request, slug, pk):
	items_done = 0;
	items_today = 0;
	items_important = 0;

	list = get_object_or_404(List, pk=pk)
	lists = List.objects.all().filter(owner=request.user)
	items = Item.objects.filter(published_date__lte=timezone.now(), list_id=list).order_by('end_date')
	
	for elem in lists:
		if slug == elem.slug:
			elem.active = True
		else:
			elem.active = False
		elem.save()

	for item in items: 
		if item.checked:
			items_done += 1
		if (item.end_date.date() - timezone.now().date()).days < 1:
			items_today += 1
		if item.important:
			items_important += 1

	list_info = {
		'items_done': items_done,
		'item_count': items.count(),
		'items_today': items_today,
		'items_important': items_important,
	}
	
	list_form = ListForm()
	item_form = ItemForm()

	return render(request, 'list/list.html', {
		'list' : list,
		'lists': lists,
		'items': items,
		'list_info': list_info,
		'list_form': list_form,
		'item_form': item_form
	})

def item_detail(request, pk):
	item = get_object_or_404(Item, pk=pk)
	return render(request, 'list/item_detail.html', {'item': item})

def toggle_done(request):
	pk = request.GET.get('pk', None)
	item = Item.objects.get(pk=pk)
	item.checked = False if item.checked else True
	item.save()
	nrChecked = Item.objects.filter(checked=True).count()
	return JsonResponse({
			'pk':pk,
			'nrChecked':nrChecked
		})

def add_item(request):
	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			item = form.save(commit = False)
			item.author = request.user
			item.list_id = List.objects.get(active=True)
			item.published_date = timezone.now()
			item.save()
	return JsonResponse({
			'committed': True
		})

def remove_item(request):
	pk = request.GET.get('pk', None)
	item = Item.objects.get(pk=pk)
	item.delete()
	return JsonResponse({
			'pk':pk
		})

def add_list(request):
	if request.method == 'POST':
		form = ListForm(request.POST)
		if form.is_valid():
			list = form.save(commit = False)
			list.owner = request.user
			list.slug = slugify(form.cleaned_data['title'])
			list.save()
	return JsonResponse({
			'committed': True,
			'pk': list.pk,
			'slug': list.slug,
			'title': form.cleaned_data['title'],
		})

def remove_list(request):
	pk = request.GET.get('pk', None)
	list = List.objects.get(pk=pk)
	list.delete()
	return JsonResponse({
			'pk': pk
		})

def log_out(request):
	logout(request)
	return redirect('new')
