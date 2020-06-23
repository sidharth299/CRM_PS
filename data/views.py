import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from data.models import Person, Client, Product

@login_required(login_url='/login/')
def get_contact_person(request, name):
	
	temp = Person.objects.filter(client_name = name).all()
	contact_list = []
	for i in temp:
		contact_list.append(i.name)
	data ={}
	data['contact_list'] = contact_list
	
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type="application/json")

@login_required(login_url='/login/')
def get_contact_person_detail(request, name):
	
	temp = Person.objects.filter(name = name).first()
	data ={}
	data['email'] = temp.email
	data['telephone'] = temp.telephone_main
	
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type="application/json")

@login_required(login_url='/login/')
def get_gstin(request, name):
	
	temp = Client.objects.get(pk = name)
	data ={}
	data['gstin'] = temp.gstin
	
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type="application/json")

@login_required(login_url='/login/')
def get_basic_rate(request, name):
	
	temp = Product.objects.get(pk = name)
	data ={}
	data['basic_rate'] = temp.basic_rate
	
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type="application/json")

@login_required(login_url='/login/')
def get_city(request, name):
	
	temp = Client.objects.get(pk = name)
	data ={}
	data['city'] = temp.city
	
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type="application/json")