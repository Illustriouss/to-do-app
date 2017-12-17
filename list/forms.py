from django import forms
from .models import List
from .models import Item

class ItemForm(forms.ModelForm):

	class Meta:
		model = Item
		fields = ('title', 'place', 'end_date', 'important')

class ListForm(forms.ModelForm):
	class Meta:
		model = List
		fields = ('title',)