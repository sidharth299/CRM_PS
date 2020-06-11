from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_index, name='report_index'),
    path('line_chart/', views.line_chart, name='line_chart'),
]