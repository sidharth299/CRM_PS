from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Malhar Industries CRM'
admin.site.site_title = 'Malhar Industries CRM'

urlpatterns = [
	# changed this from the default 'admin/' url to -> ''
    path('', admin.site.urls),
    path('report/', include('report.urls')),
]
