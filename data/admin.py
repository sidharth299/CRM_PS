from django import forms
from django.db import models
from django.contrib import admin, messages
from django.forms import TextInput, Textarea

import csv
from django.http import HttpResponse

# for admin logs
from django.contrib.admin.models import LogEntry

from .models import *
from .dbconf import *

class ProductAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.DecimalField: {'widget': TextInput(attrs={'size':'20'})},
		models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
	fieldsets = [
		(None,			{'fields': ['product_name','product_category','hsn_code']}),
		('Cost and Tax', {'fields': ['basic_rate','tax_rate','export_tax_rate']}),
		(None,		{'fields' : ['remarks']})	
		]
	readonly_fields = ()

	# advantage of using this that we can disable selected fields
	
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		disable_fields = [
						'product_name',
						'product_category',
						'hsn_code',
						'basic_rate',
						'tax_rate',
						'export_tax_rate',
						'remarks']
		# change this to add custom fields
		response = valid_action(request, form, disable_fields)

		form = response

		return form
	

	def save_model(self, request, obj, form, change):
		# editing form after submission
		#obj.hsn_code = 3244
		obj.created_by = request.user
		super(ProductAdmin, self).save_model(request, obj, form, change)

	##############     for filtering            ##########333
	#list_display = ('title','created_date','tax')

class ClientAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.DecimalField: {'widget': TextInput(attrs={'size':'20'})},
		models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
	fieldsets = [
		(None,			{'fields': ['client_name','client_category','btc','gstin']}),
		('Contact', {'fields': ['contact_person','telephone_main','telephone_extra','email']}),
		('Address',		{'fields' : ['address','city','pin_code','state','country','zone']}),
		('Lead Details', {'fields' : ['lead_source','client_rank','remarks']}),
		]
	readonly_fields = ('balance','latest_dsr_id')
	list_display = ('client_name','client_category','zone')
	

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		# do not add anything here which is already in readonly list
		disable_fields = [
						'client_name',
						'client_category',
						'btc',
						'gstin',
						'contact_person',
						'telephone_main',
						'telephone_extra',
						'email',
						'address',
						'city',
						'state',
						'pin_code',
						'city',
						'country',
						'zone',
						'lead_source',
						'client_rank',
						'remarks']
		# change this to add custom fields
		response = valid_action(request, form, disable_fields)

		form = response

		return form
	

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super(ClientAdmin, self).save_model(request, obj, form, change)

class DsrAdmin(admin.ModelAdmin):
	raw_id_fields = ('client_id',)
	readonly_fields = ('created_by',)

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super(DsrAdmin, self).save_model(request, obj, form, change)

class SampleAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.DecimalField: {'widget': TextInput(attrs={'size':'20'})},
		models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
	
	readonly_fields = ('created_by',)

	# advantage of using this that we can disable selected fields
	
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		# do not add anything here which is already in readonly list
		disable_fields = [
						'client_id',
						'sent_date',
						'city',
						'product_id',
						'sample_quantity',
						'sample_status',
						'remarks'
						]
		# change this to add custom fields
		response = valid_action(request, form, disable_fields)

		form = response

		return form
	

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super(SampleAdmin, self).save_model(request, obj, form, change)


class SaleAdmin(admin.ModelAdmin):
	pass
class BillAdmin(admin.ModelAdmin):
	pass
class PaymentAdmin(admin.ModelAdmin):
	pass

class LogEntryAdmin(admin.ModelAdmin):

	date_hierarchy = 'action_time'

	#readonly_fields = LogEntry._meta.get_all_field_names()

	list_filter = [
	    'user',
	    'content_type',
	    'action_flag'
	]

	search_fields = [
	    'object_repr',
	    'change_message'
	]


	list_display = [
	    'action_time',
	    'user',
	    'content_type',
	    'action_flag_',
	    'change_message',
	]

	def has_add_permission(self, request):
	    return False

	def has_change_permission(self, request, obj=None):
	    return request.user.is_superuser and request.method != 'POST'

	def has_delete_permission(self, request, obj=None):
	    return False

	def action_flag_(self, obj):
	    flags = {
	        1: "Addition",
	        2: "Changed",
	        3: "Deleted",
	    }
	    return flags[obj.action_flag]
	"""
	def object_link(self, obj):
	    if obj.action_flag == DELETION:
	        link = escape(obj.object_repr)
	    else:
	        ct = obj.content_type
	        link = u'<a href="%s">%s</a>' % (
	            reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
	            escape(obj.object_repr),
	        )
	    return link
	object_link.allow_tags = True
	object_link.admin_order_field = 'object_repr'
	object_link.short_description = u'object'
	"""

# just comment the line of the model below you want to hide from the admin dashboard

admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)

admin.site.register(LogEntry, LogEntryAdmin)

admin.site.register(Dsr,DsrAdmin)
admin.site.register(Sample,SampleAdmin)
admin.site.register(Sale,SaleAdmin)
admin.site.register(Bill,BillAdmin)
admin.site.register(Payment,PaymentAdmin)
