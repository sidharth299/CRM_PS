from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .dbconf import *

class ProductAdmin(admin.ModelAdmin):
	formfield_overrides = FORMFIELD_OVERRIDES
	fieldsets = [
		(None,			{'fields': ['product_name','product_category','hsn_code']}),
		('Cost and Tax', {'fields': ['basic_rate','tax_rate','export_tax_rate']}),
		(None,		{'fields' : ['remarks']})
		]
	readonly_fields = ()

	list_display = [
		'product_name',
		'product_category',
		'hsn_code'
	]

	list_filter = [
		'product_category',
	]

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'product'
		form = customized_form(request,form,name, dfields)
		return form

	def save_model(self, request, obj, form, change):
		# editing form after submission
		obj.created_by = request.user
		super(ProductAdmin, self).save_model(request, obj, form, change)

class ClientAdmin(admin.ModelAdmin):
	# formfield_overrides = FORMFIELD_OVERRIDES
	
	fieldsets = [
		(None,			{'fields': ['client_name','client_category','btc','gstin']}),
		('Contact', {'fields': ['contact_person','telephone_main','telephone_extra','email']}),
		('Address',		{'fields' : ['address','city','pin_code','state','country','zone']}),
		('Lead Details', {'fields' : ['lead_source','client_rank','remarks','balance']}),
		]
	readonly_fields = ('balance',)
	list_display = ('client_name','client_category','zone', 'client_rank', 'telephone_main')

	list_filter = [
		'client_category',
		'btc',
		'client_rank',
		'zone',
	]

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'client'
		form = customized_form(request,form,name, dfields)
		return form

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super(ClientAdmin, self).save_model(request, obj, form, change)


class SampleAdmin(admin.ModelAdmin):
	# formfield_overrides = FORMFIELD_OVERRIDES

	list_filter = [
		'sample_status',
		'product_name',
		('sent_date', DateFieldListFilter),
	]

	list_display = [
		'client_name',
		'product_name',
		'sample_status',
		'sent_date',
	]
	
	readonly_fields = ('created_by',)

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'sample'
		form = customized_form(request,form,name, dfields)
		return form

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super(SampleAdmin, self).save_model(request, obj, form, change)


class TargetAdmin(admin.ModelAdmin):
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'target'
		form = customized_form(request,form,name, dfields)
		return form
	

class EntryAdmin(admin.ModelAdmin):
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'entry'
		form = customized_form(request,form,name, dfields)
		return form