from django.db import models
from django.utils import timezone

class List(models.Model):
	owner = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	slug = models.SlugField()
	active = models.BooleanField(default=False)

	def isActive(self):
		if self.active:
			return "list--active"
		return ""

	def __str__(self):
		return self.title

class Item(models.Model):
	author = models.ForeignKey('auth.User')
	list_id = models.ForeignKey(List)
	title = models.CharField(max_length=200)
	place = models.CharField(max_length=200, null=True)
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	end_date = models.DateTimeField(blank=True, null=True)
	checked = models.BooleanField(default=False)
	important = models.BooleanField(default=False)
	today = models.BooleanField(default=False)

	def publish(self):
		self.published_date = timezone.now()

	def isImportant(self):
		if self.important:
			return "item--important"
		return ""

	def isDone(self):
		if self.checked:
			return "item--checked"
		return ""

	def setChecked(self):
		self.checked = True

	def setUnChecked(self):
		self.checked = False
 
	def getPlace(self):
		if self.place == None:
			return ""
		return "at "+self.place

	def getUntilDate(self):
		if self.end_date == None:
			return ""
		until_date = (self.end_date.date() - timezone.now().date()).days
		if until_date > 1:
			return "in " + str(until_date) + " days"
		if until_date == 1:
			return	"in " + str("1 day")
		if until_date < 1:
			return "today"

	def __str__(self):
		return self.title