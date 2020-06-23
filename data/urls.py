from django.urls import path
from . import views

urlpatterns = [
	path('get_contact_person/<str:name>/', views.get_contact_person, name='get_contact_person'),
	path('get_contact_person_detail/<str:name>/', views.get_contact_person_detail, name='get_contact_person_detail'),
	path('get_gstin/<str:name>/', views.get_gstin, name='get_gstin'),
	path('get_basic_rate/<str:name>/', views.get_basic_rate, name='get_basic_rate'),
	path('get_city/<str:name>/', views.get_city, name='get_city')
]