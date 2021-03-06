# admin log
from django.contrib.admin.models import LogEntry
# required for joining with admin log
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from django.apps import apps
from django.forms import TextInput, Textarea
from datetime import date

from .models import *

FORMFIELD_OVERRIDES = {
	models.DecimalField: {'widget': TextInput(attrs={'size':'20'})},
	models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
    models.CharField: {'widget': TextInput(attrs={'size':'40'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
}

def valid_action(request, form, disable_fields):
	response = form
	message_dict = request._messages.__dict__

	keyword = request.path.split('/')
	"""
	example: /data/product/1/change/    
	app label = data, model = product, object_id = 1, action = change
	"""
	model = keyword[2]
	object_id = keyword[3]
	action = keyword[4]
	user_id = request.user.id

	if len(keyword) >= 5 and action=='change' and not request.user.is_superuser:
		res = LogEntry.objects.filter(content_type__model=model, object_id=object_id, action_flag = 1).first()
		# first check if the user is the creator of the object or not
		if res.user_id != user_id or (timezone.now()-res.action_time).days > 0:
			for i in disable_fields:
				if i in form.base_fields:
					form.base_fields[i].disabled = True
			response = form
		error_message = False
		if res.user_id != user_id and not message_dict['added_new']:
			error_message = 'This record was not created by you. If you want to update it, please contact the admininstrator'
		elif (timezone.now()-res.action_time).days > 0 and not message_dict['added_new']:
			error_message = 'This record was created 24 hours ago. If you want to update it, please contact the admininstrator'
		else:
			pass
		
		if error_message:
			messages.add_message(request, messages.INFO, error_message)

	return response

def customized_form(request, form, name, dfields):
	keyword = request.path.split('/')
	action = keyword[4]
	if action == 'change':
		for i in dfields:
			if i in form.base_fields:
				form.base_fields[i].disabled = True

	if request.user.has_perm('data.change_'+name):
		model = apps.get_model('data', name)
		disable_fields = [field.name for field in model._meta.get_fields()]
		form = valid_action(request, form, disable_fields)

	return form

def validate_date(date):
	current_date = date.today()
	if date > current_date:
		error_message = 'Please do not enter a future date'
		return error_message
	month = current_date.month
	flag = False
	if month in [1,2,3]:
		if date.month in [1,2,3]:
			if date.year == current_date.year:
				flag = True
		else:
			if date.year == current_date.year-1:
				flag = True
	else:
		if not (date.month in [1,2,3]):
			if date.year == current_date.year:
				flag = True
	if not flag and not user_session['is_superuser']:
		error_message = 'Please do not enter a date of previous financial year. Contact admininstrator if you want to'
		return error_message

	return False 
