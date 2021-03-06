from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_index, name='report_index'),
    path('line_chart/', views.line_chart, name='line_chart'),
    path('sample_report/', views.sample_report, name='sample_report'),
    path('rank_register/', views.rank_register, name='rank_register'),
    path('industry_sales/', views.industry_sales, name='industry_sales'),
    path('item_sales/', views.item_sales, name='item_sales'),
    path('outstanding_report/', views.outstanding_report, name='outstanding_report'),
    path('payment_register/', views.payment_register, name='payment_register'),
    path('daily_sales/', views.daily_sales, name='daily_sales'),
    path('perf_report/', views.perf_report, name='perf_report'),
    path('strategic_report/', views.strategic_report, name='strategic_report')
]