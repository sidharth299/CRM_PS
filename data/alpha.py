# import csv
# from django.http import HttpResponse
from django.forms import TextInput, Textarea
from django.contrib import admin
from .dbconf import *
from django.db.models import Sum


class DsrAdmin(admin.ModelAdmin):
	#autocomplete_fields = ['client_name']
	raw_id_fields = ('client_name',)
	readonly_fields = ('created_by',)

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
			client = Client.objects.get(pk = obj.client_name)
			if obj.contact_person == '':
				obj.contact_person = client.contact_person
			if obj.telephone == '':
				obj.telephone = client.telephone_main
			if obj.email == '':
				obj.email = client.email
		# print((self.model.objects.get(id=obj.id)).contact_person)
		super(DsrAdmin, self).save_model(request, obj, form, change)

class BillInline(admin.TabularInline):

	model = Bill
	extra = 1
	#readonly_fields = ('')

class SaleAdmin(admin.ModelAdmin):
	raw_id_fields = ('client_name',)
	readonly_fields = ('amount_paid','first_date','last_date','created_by','sgst','igst','cgst','export_sale','total_amount')
	inlines = [BillInline]

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		# do not add anything here which is already in readonly list
		disable_fields = [
					'client_name'
						]
		response = valid_action(request, form, disable_fields)

		form = response

		return form
	
	def save_formset(self, request, form, formset, change):
		
		instances = formset.save(commit=False)
		request_dict = request.POST
		print(request_dict)
		# that is some new record
		if not change:
			amount = 0
			for instance in instances:
				product = Product.objects.get(pk=instance.product_name)
				if instance.basic_rate == None:
					instance.basic_rate = product.basic_rate
				amount+=instance.basic_rate*instance.quantity
				instance.save()
			
			temp = Bill.objects.order_by('-id')[0]
			invoice_id = temp.invoice_number_id

			product = Product.objects.get(pk=temp.product_name)
			tax_rate = product.tax_rate
			export_tax_rate = product.export_tax_rate

			invoice = Sale.objects.get(pk=invoice_id)
			total_amount = amount + invoice.carting
			basic_tax = (total_amount*tax_rate)/100
			export_tax = (total_amount*export_tax_rate)/100
			tax_type = invoice.tax_type
			if tax_type == 'Maharashtra':
				invoice.cgst = round(basic_tax/2,2)
				invoice.sgst = round(basic_tax/2,2)
				invoice.igst = 0
				invoice.export_sale = 0
			else:
				invoice.cgst = 0
				invoice.sgst = 0
				if tax_type == 'Outside Maharashtra':
					invoice.igst = round(basic_tax,2)
					invoice.export_sale = 0
				elif tax_type == 'Indirect Export':
					invoice.igst = round(export_tax,2)
					invoice.export_sale = 0
				else:
					invoice.igst = round(export_tax,2)
					invoice.export_sale = round(export_tax,2)
			invoice.total_amount = round(total_amount + invoice.cgst + invoice.igst + invoice.sgst - invoice.export_sale)
			invoice.save()
			
			client = Client.objects.get(pk = invoice.client_name)
			client.balance = client.balance + invoice.total_amount
			client.save()
		
		# for change
		if change:
			for instance in instances:
				product = Product.objects.get(pk=instance.product_name)
				if instance.basic_rate == None:
					instance.basic_rate = product.basic_rate
				instance.save()
			
			keyword = request.path.split('/')
			invoice_id = keyword[3]
			# amount = Bill.objects.filter(invoice_number_id = invoice_id).aggregate(Sum(F('basic_rate')*F('quantity')))
			products= Bill.objects.filter(invoice_number_id = invoice_id)
			amount = 0
			for product in products:
				amount = amount + (product.quantity*product.basic_rate)

			temp = Bill.objects.filter(invoice_number_id = invoice_id).first()
			product = Product.objects.get(pk=temp.product_name)
			tax_rate = product.tax_rate
			export_tax_rate = product.export_tax_rate

			invoice = Sale.objects.get(pk=invoice_id)
			total_amount = amount + invoice.carting
			print(total_amount)
			basic_tax = (total_amount*tax_rate)/100
			export_tax = (total_amount*export_tax_rate)/100
			tax_type = invoice.tax_type
			if tax_type == 'Maharashtra':
				invoice.cgst = round(basic_tax/2,2)
				invoice.sgst = round(basic_tax/2,2)
				invoice.igst = 0
				invoice.export_sale = 0
			else:
				invoice.cgst = 0
				invoice.sgst = 0
				if tax_type == 'Outside Maharashtra':
					invoice.igst = round(basic_tax,2)
					invoice.export_sale = 0
				elif tax_type == 'Indirect Export':
					invoice.igst = round(export_tax,2)
					invoice.export_sale = 0
				else:
					invoice.igst = round(export_tax,2)
					invoice.export_sale = round(export_tax,2)

			old_amount = invoice.total_amount
			invoice.total_amount = round(total_amount + invoice.cgst + invoice.igst + invoice.sgst - invoice.export_sale)
			new_amount = invoice.total_amount
			# updating amount_paid column
			if old_amount != new_amount:
				payments = Payment.objects.filter(invoice_number_id = invoice_id)
				count = 0
				for payment in payments:
					count = count + payment.amount_received
				invoice.amount_paid = count
			invoice.save()

			client = Client.objects.get(pk = invoice.client_name)
			client.balance = client.balance + new_amount - old_amount
			client.save()

		formset.save_m2m()
	
	def save_model(self, request, obj, form, change):
		
		# means adding a new record not updating		
		if not change:
			obj.created_by = request.user
			obj.igst = 0
			obj.cgst = 0
			obj.sgst = 0
			obj.export_sale = 0
			obj.total_amount = 0

		if change:
			pass

		super(SaleAdmin, self).save_model(request, obj, form, change)

	def delete_model(self, request, obj):
		keyword = request.path.split('/')
		obj_id = keyword[3]
		sale = Sale.objects.get(pk=obj_id)
		client = Client.objects.get(pk = sale.client_name)
		client.balance = client.balance - sale.total_amount
		client.save()
		super(SaleAdmin, self).delete_model(request, obj)

class PaymentAdmin(admin.ModelAdmin):
	raw_id_fields = ('invoice_number',)
	readonly_fields = ('created_by',)

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		# do not add anything here which is already in readonly list
		disable_fields = [
					'invoice_number',
					'amount_received'
						]
		response = valid_action(request, form, disable_fields)
		form = response
		return form
	
	def save_model(self, request, obj, form, change):
		
		# means adding a new record not updating		
		if not change:
			obj.created_by = request.user
			
			invoice = obj.invoice_number
			if invoice.amount_paid == 0:
				invoice.first_date = obj.date
			invoice.amount_paid = obj.amount_received
			if invoice.amount_paid - invoice.total_amount <=0:
				invoice.last_date = obj.date

			invoice.save()

			client = Client.objects.get(pk = invoice.client_name)
			client.balance = client.balance - obj.amount_received
			client.save()
			
		if change:
			keyword = request.path.split('/')
			payment_id = keyword[3]
			payment = Payment.objects.get(pk = payment_id)
			old_amount = payment.amount_received
			new_amount = obj.amount_received

			if old_amount != new_amount:
				invoice = obj.invoice_number
				if invoice.amount_paid == 0:
					invoice.first_date = obj.date
				invoice.amount_paid = invoice.amount_paid - old_amount + new_amount
				if invoice.amount_paid - invoice.total_amount <= 0:
					invoice.last_date = obj.date

				invoice.save()

				client = Client.objects.get(pk = invoice.client_name)
				client.balance = client.balance + old_amount - new_amount
				client.save()

		super(PaymentAdmin, self).save_model(request, obj, form, change)
	
	def delete_model(self, request, obj):
		keyword = request.path.split('/')
		payment_id = keyword[3]
		payment = Payment.objects.get(pk = payment_id)
		old_amount = payment.amount_received

		invoice = obj.invoice_number
		if invoice.amount_paid == 0:
			invoice.first_date = obj.date
		invoice.amount_paid = invoice.amount_paid - old_amount
		if invoice.amount_paid - invoice.total_amount <=0:
			invoice.last_date = obj.date

		invoice.save()

		client = Client.objects.get(pk = invoice.client_name)
		client.balance = client.balance + old_amount
		client.save()
		super(PaymentAdmin, self).delete_model(request, obj)

"""
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