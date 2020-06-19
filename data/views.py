import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from data.models import Person

@login_required(login_url='/login/')
def get_contact_person(request, name):
	
	temp = Person.objects.filter(client_name = name).all()
	contact_list = []
	for i in temp:
		contact_list.append(i.name)
	data = {'contact_list':contact_list}
	json_data = json.dumps(data)

	return HttpResponse(json_data, content_type="application/json")