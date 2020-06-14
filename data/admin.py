# from django import forms
# import csv
# from django.http import HttpResponse
# from django.db import models
# from django.contrib import admin
# from .models import *
# ALL OF THE HEADRES ABOVE ARE REDUNDANT

# alpha has all classes except DsrAdmin and SampleAdmin
from .alpha import *
# beta has DsrAdmin and SampleAdmin
from .beta import *

# just comment the line of the model below you want to hide from the admin dashboard

admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)

admin.site.register(LogEntry, LogEntryAdmin)

admin.site.register(Dsr,DsrAdmin)
admin.site.register(Sample,SampleAdmin)
admin.site.register(Sale,SaleAdmin)
admin.site.register(Payment,PaymentAdmin)