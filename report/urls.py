from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_index, name='report_index'),
    path('line_chart/', views.line_chart, name='line_chart'),
    path('sample_report/', views.sample_report, name='sample_report'),
    path('rank_register/', views.rank_register, name='rank_register')
]