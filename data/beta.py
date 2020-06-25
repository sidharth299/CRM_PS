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

	def get_queryset(self, request):
		qs = super(ClientAdmin, self).get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(assign__assigned_to = request.user)
		return qs

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'client'
		form = customized_form(request,form,name, dfields)
		return form

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
			c = Assign(client_name = obj, created_by = request.user, assigned_to = request.user)
			c.save()
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

	def get_queryset(self, request):
		qs = super(SampleAdmin, self).get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(client_name__in = (Client.objects.filter(assign__assigned_to = request.user).all()))
		return qs

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

	def get_queryset(self, request):
		qs = super(TargetAdmin, self).get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(user_id = request.user)
		return qs

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'target'
		form = customized_form(request,form,name, dfields)
		return form

	search_fields = ('user_id__username','period')

	list_display = [
		'user_id',
		'period',
	]

class EntryAdmin(admin.ModelAdmin):

	readonly_fields = ('user_id',)
	raw_id_fields = ('client_name',)

	def get_queryset(self, request):
		qs = super(EntryAdmin, self).get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(user_id = request.user)
		return qs

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'entry'
		form = customized_form(request, form, name, dfields)
		return form

	list_display = [
		'client_name',
		'user_id',
		'entry_type',
		'entry_date'
	]

	search_fields = ('user_id__username','client_name__client_name')

	list_filter = ['entry_type', ('entry_date',DateFieldListFilter)]

	def save_model(self, request, obj, form, change):
		if not change:
			obj.user_id = request.user

		super(EntryAdmin, self).save_model(request, obj, form, change)

class AssignAdmin(admin.ModelAdmin):

	fields = ['client_name','created_by','assigned_to']
	readonly_fields = ('created_by','client_name',)

	list_display = [
		'client_name',
		'created_by',
		'assigned_to'
	]

	search_fields = ('user_id__username','client_name__client_name')

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'assign'
		form = customized_form(request, form, name, dfields)
		return form

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False