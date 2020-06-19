from django.urls import path
from . import views

urlpatterns = [
    path('get_contact_person/<str:name>/', views.get_contact_person, name='get_contact_person')
]