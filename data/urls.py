from django.urls import path

from . import views

urlpatterns = [
	path('get_contact_person/', views.get_contact_person, name='get_contact_person'),
	path('get_contact_person_detail/', views.get_contact_person_detail, name='get_contact_person_detail'),
	path('get_gstin/', views.get_gstin, name='get_gstin'),
	path('get_basic_rate/', views.get_basic_rate, name='get_basic_rate'),
	path('get_city/', views.get_city, name='get_city')
]