# admin log
from django.contrib.admin.models import LogEntry
# required for joining with admin log
from django.contrib.contenttypes.models import ContentType

# displaying messages in forms
from django.contrib import messages

from .models import *

def valid_action(request, form, disable_fields):
	response = form

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
				form.base_fields[i].disabled = True
			response = form
		error_message = False
		if res.user_id != user_id:
			error_message = 'This record was not created by you. If you want to update it, please contact the admininstrator'
		elif (timezone.now()-res.action_time).days > 0:
			error_message = 'This record was created 24 hours ago. If you want to update it, please contact the admininstrator'
		else:
			pass
		if error_message:
			messages.add_message(request, messages.INFO, error_message)

	return response