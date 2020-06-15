from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_index, name='report_index'),
    path('line_chart/', views.line_chart, name='line_chart'),
    path('sample_report/', views.sample_report, name='sample_report'),
    path('rank_register/', views.rank_register, name='rank_register'),
    path('industry_sales/', views.industry_sales, name='industry_sales'),
    path('item_sales/', views.item_sales, name='item_sales'),
    path('outstanding_report/', views.outstanding_report, name='outstanding_report')
]