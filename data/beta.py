# import csv
# from django.http import HttpResponse
from django.forms import TextInput, Textarea
from django.contrib import admin

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
	
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)

		# list of fileds that needs to be disabled (in this case all fields except readonly_fields)
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

		response = valid_action(request, form, disable_fields)

		form = response

		return form
	

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super(ClientAdmin, self).save_model(request, obj, form, change)


class SampleAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.DecimalField: {'widget': TextInput(attrs={'size':'20'})},
		models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
	
	readonly_fields = ('created_by',)
	
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		# do not add anything here which is already in readonly list
		disable_fields = [
						'client_name',
						'sent_date',
						'city',
						'product_name',
						'sample_quantity',
						'sample_status',
						'remarks'
						]
		response = valid_action(request, form, disable_fields)

		form = response

		return form
	

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super(SampleAdmin, self).save_model(request, obj, form, change)