from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .dbconf import *

class ProductAdmin(admin.ModelAdmin):
	# formfield_overrides = FORMFIELD_OVERRIDES
	fieldsets = [
		(None,			{'fields': ['product_name','product_category','hsn_code']}),
		('Cost and Tax', {'fields': ['basic_rate','tax_rate','export_tax_rate','remarks','created_by']}),
		]
	readonly_fields = ('created_by',)
	search_fields = ('product_name','hsn_code')

	list_display = [
		'product_name',
		'product_category',
		'hsn_code'
	]

	list_filter = [	'product_category',]

	search_fields = ('product_name',)

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'product'
		form = customized_form(request,form,name, dfields)
		return form

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
		super(ProductAdmin, self).save_model(request, obj, form, change)

class ClientAdmin(admin.ModelAdmin):

	fieldsets = [
		(None, {'fields': ['client_name','client_category','btc','gstin','balance']}),
		('Contact', {'fields': ['telephone_main','telephone_extra','email']}),
		('Address',	{'fields' : ['address','city','pin_code','state','country','zone']}),
		('Lead Details', {'fields' : ['lead_source','client_rank','remarks','created_by']}),
		]
	readonly_fields = ('balance','client_rank','created_by')

	search_fields = ('client_name', 'telephone_main')

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
		if not change:
			obj.created_by = request.user
		super(ClientAdmin, self).save_model(request, obj, form, change)


class SampleAdmin(admin.ModelAdmin):
	fieldsets = [
		('Client Details', {'fields': ['client_name','city']}),
		('Sample Details', {'fields': ['sent_date','product_name','sample_quantity','sample_status','remarks','created_by']}),
		]

	readonly_fields = ('created_by',)
	raw_id_fields = ('client_name','product_name')

	search_fields = ('client_name__client_name', 'product_name__product_name')

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

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'sample'
		form = customized_form(request,form,name, dfields)
		return form

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
			client = obj.client_name
			if obj.city == '':
				obj.city = client.city

		super(SampleAdmin, self).save_model(request, obj, form, change)

class TargetAdmin(admin.ModelAdmin):

	fieldsets = [
		('User Information', {'fields': ['user_id', 'period',]}),
		(None, {'fields': ['big', 'other', 'sale_value',]} ),
		(None, {'fields': ['lead_gen','mnoc', 'hit_ratio',]} ),
		('Sales Type', {'fields': ['cross_sale', 'ref_sale', 'up_sale', 'lost_sale', 'rank_6_7',]}),
		(None, {'fields': ['d_appointment', 'appr_letter',]} ),
		(None, {'fields': ['ats', 'total_outstanding',]} ),
		('MTD', {'fields': ['MTD_sales', 'MTD_collection',]} ),
	]

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'target'
		form = customized_form(request,form,name, dfields)
		return form

	list_display = [
		'user_id',
		'period',
	]

class EntryAdmin(admin.ModelAdmin):

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'entry'
		form = customized_form(request,form,name, dfields)
		return form

	list_display = [
		'user_id',
		'entry_type',
		'entry_date'
	]

	search_fields = ('user_id__username',)

	list_filter = ['entry_type', ('entry_date',DateFieldListFilter)]
