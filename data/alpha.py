from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .dbconf import *
from .filters import *

class DsrAdmin(admin.ModelAdmin):

	raw_id_fields = ('client_name','product_name')
	readonly_fields = ('created_by',)

	list_display = ['client_name', 'date_of_contact', 'action', 'next_call_date']

	list_filter = ['contact_mode', 'client_rank', 'sample_status', ]

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = []
		name = 'dsr'
		form = customized_form(request,form,name, dfields)
		return form

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

		super(DsrAdmin, self).save_model(request, obj, form, change)

class BillInline(admin.TabularInline):
	raw_id_fields = ('product_name',)
	model = Bill
	extra = 1

class SaleAdmin(admin.ModelAdmin):
	raw_id_fields = ('client_name',)
	readonly_fields = ('invoice_number','amount_paid','first_date','last_date','created_by','sgst','igst','cgst','export_sale','total_amount')

	list_filter = (AdvanceInvoiceListFilter, 'tax_type', ('sale_date', DateFieldListFilter))
	inlines = [BillInline]

	list_display = ['invoice_number', 'client_name', 'total_amount', 'sale_date']

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = ['client_name']
		name = 'sale'
		form = customized_form(request,form,name, dfields)
		return form

	def save_formset(self, request, form, formset, change):

		instances = formset.save(commit=False)
		request_dict = dict(request.POST)
		# new record
		if not change:
			amount = 0
			for instance in instances:
				product = Product.objects.get(pk=instance.product_name)
				if instance.basic_rate == None:
					instance.basic_rate = product.basic_rate
				amount+=instance.basic_rate*instance.quantity
				instance.save()


			invoice_id = (Sale.objects.all().last()).invoice_number
			temp = Bill.objects.filter(invoice_number_id = invoice_id).first()
			if temp != None:
				product = Product.objects.get(pk=temp.product_name)
				tax_rate = product.tax_rate
				export_tax_rate = product.export_tax_rate
			else:
				tax_rate = 0
				export_tax_rate = 0

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

		# updating record
		if change:
			for instance in instances:
				product = Product.objects.get(pk=instance.product_name)
				if instance.basic_rate == None:
					instance.basic_rate = product.basic_rate
				instance.save()

			keyword = request.path.split('/')
			invoice_id = keyword[3]
			products= Bill.objects.filter(invoice_number_id = invoice_id)
			amount = 0
			for product in products:
				amount = amount + (product.quantity*product.basic_rate)
			""" function to delete any sub elements (products) okay """

			i = 1
			while True:

				if not ('bill_set-'+str(i)+'-id' in request_dict):
					break
				if 'bill_set-'+str(i)+'-DELETE' in request_dict:
					if request_dict['bill_set-'+str(i)+'-DELETE'] == ['on']:

						amount = amount - int(request_dict['bill_set-'+str(i)+'-quantity'][0])*int(request_dict['bill_set-'+str(i)+'-basic_rate'][0])
						bill = Bill.objects.get(pk = int(request_dict['bill_set-'+str(i)+'-id'][0]))
						bill.delete()
				i = i+1

			"""function end"""
			temp = Bill.objects.filter(invoice_number_id = invoice_id).first()
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

		# new record
		if not change:
			obj.created_by = request.user
			obj.igst = 0
			obj.cgst = 0
			obj.sgst = 0
			obj.export_sale = 0
			obj.total_amount = 0
		# updating record
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

	list_display = ['invoice_number', 'amount_received', 'date']

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		dfields = ['invoice_number']
		name = 'payment'
		form = customized_form(request,form,name, dfields)
		return form

	def save_model(self, request, obj, form, change):

		# new record
		if not change:
			obj.created_by = request.user

			invoice = obj.invoice_number
			if invoice.amount_paid >= 0:
				invoice.first_date = obj.date
			invoice.amount_paid = obj.amount_received
			if invoice.amount_paid - invoice.total_amount >=0 and invoice.total_amount > 0:
				invoice.last_date = obj.date

			invoice.save()

			client = Client.objects.get(pk = invoice.client_name)
			client.balance = client.balance - obj.amount_received
			client.save()
		# updating record
		if change:
			keyword = request.path.split('/')
			payment_id = keyword[3]
			payment = Payment.objects.get(pk = payment_id)
			old_amount = payment.amount_received
			new_amount = obj.amount_received

			if old_amount != new_amount:
				invoice = obj.invoice_number
				if invoice.amount_paid >= 0:
					invoice.first_date = obj.date
				invoice.amount_paid = invoice.amount_paid - old_amount + new_amount
				if invoice.amount_paid - invoice.total_amount >= 0 and invoice.total_amount > 0 :
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
		if invoice.amount_paid >= 0:
			invoice.first_date = obj.date
		invoice.amount_paid = invoice.amount_paid - old_amount
		if invoice.amount_paid - invoice.total_amount >=0 and invoice.total_amount > 0:
			invoice.last_date = obj.date

		invoice.save()

		client = Client.objects.get(pk = invoice.client_name)
		client.balance = client.balance + old_amount
		client.save()
		super(PaymentAdmin, self).delete_model(request, obj)