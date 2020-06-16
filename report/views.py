import csv
import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from report.forms import *
from data.models import *

@login_required(login_url='/login/')
def report_index(request):
	return render(request,'report/report_index.html',{})

@login_required(login_url='/login/')
def line_chart(request):
	payload = {}

	if request.method == 'POST':
		form = LineChart(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_date = form.cleaned_data['start_date']
			last_date = form.cleaned_data['end_date']
			is_csv = form.cleaned_data['is_csv']

			user_id = (User.objects.filter(username=username).first()).id

			# count is referred as calls here
			# 1 visit -> 1 call
			# other mode of communication -> 1/3 call

			# using RAW SQL in django
			res = Dsr.objects.raw('''SELECT  id,date_of_contact,
									SUM(CASE WHEN contact_mode = 'Visit' THEN 3
											WHEN contact_mode in ('Telephone','Email','WhatsApp') THEN 1
											ELSE 0 END) 
									AS count 
									FROM data_dsr
									WHERE created_by_id = '{0}' AND (date_of_contact BETWEEN '{1}' AND '{2}')
									GROUP BY date_of_contact
									'''.format(user_id,first_date,last_date)
								)
			for r in res:
				r.count = round(r.count/3,2)

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="LineChart.csv"'

				writer = csv.writer(response)
				# adding headres
				writer.writerow(['Date of Contact','Number of Calls'])
				for r in res:
					writer.writerow([r.date_of_contact,r.count])
				return response


			payload = {'report':res,'username':username}
			return render(request,'report/line_chart.html',payload)
		else:
			payload['form'] = LineChart()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = LineChart()
	
	return render(request,'report/report_form.html',payload)

@login_required(login_url='/login/')
def sample_report(request):
	payload = {}

	if request.method == 'POST':
		form = SampleReport(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_date = form.cleaned_data['start_date']
			last_date = form.cleaned_data['end_date']

			user_id = (User.objects.filter(username=username).first()).id

			# using RAW SQL in django
			res = Sample.objects.raw('''SELECT  data_sample.id, sent_date, data_client.client_name as client, data_sample.city, data_product.product_name as product, data_sample.sample_quantity, data_sample.sample_status
									FROM data_sample join data_product on data_product.product_name=data_sample.product_name_id join data_client on data_client.client_name = data_sample.client_name_id
									WHERE data_sample.created_by_id = '{0}' AND (sent_date BETWEEN '{1}' AND '{2}') order by sent_date
									'''.format(user_id,first_date,last_date)
								)


			res2 = Sample.objects.raw('''SELECT  id, sample_status, count(id) as count
									FROM data_sample
									WHERE created_by_id = '{0}' AND (sent_date BETWEEN '{1}' AND '{2}') group by sample_status
									'''.format(user_id,first_date,last_date)
								)

			payload = {'report':res,'report2':res2,'username':username}
			return render(request,'report/sample_report.html',payload)
		else:
			payload['form'] = SampleReport()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = SampleReport()
	
	return render(request,'report/report_form.html',payload)

@login_required(login_url='/login/')
def rank_register(request):
	payload = {}

	if request.method == 'POST':
		form = RankRegister(request.POST)
		if form.is_valid():
			rank=form.cleaned_data['rank']

			res = Client.objects.raw('''SELECT  client_name, client_category, city , telephone_main, client_rank from data_client where
										client_rank='{0}' order by client_name
									'''.format(rank,)
								)
			
			res2 = Client.objects.raw('''SELECT  client_name, count(client_name) as count from data_client where
										client_rank='{0}' order by client_name
									'''.format(rank,)
								)

			payload = {'report':res, 'report2':res2 ,'rank':rank}
			return render(request,'report/rank_register.html',payload)
		else:
			payload['form'] = RankRegister()
			return render(request,'report/report_form.html',payload)
	else:
		payload['form'] = RankRegister()
	
	return render(request,'report/report_form.html',payload)

@login_required(login_url='/login/')
def industry_sales(request):
	payload = {}

	if request.method == 'POST':
		form = IndustrySales(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_date = form.cleaned_data['start_date']
			last_date = form.cleaned_data['end_date']

			user_id = (User.objects.filter(username=username).first()).id

			# using RAW SQL in django
			res = Sale.objects.raw('''SELECT invoice_number,sale_date,client_name_id,client_category, SUM(total_amount) AS total
									FROM data_sale 
									JOIN data_client ON data_sale.client_name_id = data_client.client_name
									WHERE data_sale.created_by_id = '{0}' AND (sale_date BETWEEN '{1}' AND '{2}') GROUP BY client_name ORDER BY client_category
									'''.format(user_id,first_date,last_date)
								)	
			
			

			res2 = Sale.objects.raw('''SELECT invoice_number,client_category, SUM(total_amount) AS total
									FROM data_sale JOIN data_client ON data_sale.client_name_id = data_client.client_name
									WHERE data_sale.created_by_id = '{0}' AND (sale_date BETWEEN '{1}' AND '{2}')
									GROUP BY client_category ORDER BY SUM(total_amount)
									'''.format(user_id,first_date,last_date)
								)
			payload = {'report':res,'report2':res2,'username':username}
			return render(request,'report/industry_sales.html',payload)
		else:
			payload['form'] = IndustrySales()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = IndustrySales()

	return render(request,'report/report_form.html',payload)				
				


@login_required(login_url='/login/')
def item_sales(request):
	payload = {}

	if request.method == 'POST':
		form = ItemSales(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_date = form.cleaned_data['start_date']
			last_date = form.cleaned_data['end_date']

			user_id = (User.objects.filter(username=username).first()).id

			# using RAW SQL in django
			res = Sample.objects.raw('''SELECT  data_bill.id, data_bill.product_name_id as p, sum(data_bill.quantity) as q, sum(data_bill.basic_rate*data_bill.quantity) as t
									FROM data_bill join data_sale on data_sale.invoice_number=data_bill.invoice_number_id
									WHERE data_sale.created_by_id = '{0}' AND (data_sale.sale_date BETWEEN '{1}' AND '{2}') group by data_bill.product_name_id order by t desc
									'''.format(user_id,first_date,last_date)
								)

			payload = {'report':res, 'username':username, 'firstdate':first_date, 'lastdate':last_date}
			return render(request,'report/item_sales.html',payload)
		else:
			payload['form'] = ItemSales()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = ItemSales()
	
	return render(request,'report/report_form.html',payload)

@login_required(login_url='/login/')
def outstanding_report(request):
	payload = {}

	if request.method == 'POST':
		form = OutstandingReport(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_date = form.cleaned_data['start_date']
			last_date = form.cleaned_data['end_date']

			user_id = (User.objects.filter(username=username).first()).id

			today = datetime.date.today()
			
			cur_date=today.strftime("%Y-%m-%d")

			# using RAW SQL in django
			
			res2 = Sample.objects.raw('''SELECT invoice_number as id, client_name_id , sale_date, round(julianday('now')-julianday(sale_date)) as diff ,(total_amount-amount_paid) as b
									FROM data_sale 
									WHERE created_by_id = '{0}' AND (sale_date BETWEEN '{1}' AND '{2}') AND b>0 order by sale_date
									'''.format(user_id,first_date,last_date,)
								)

			res3 = Sample.objects.raw('''SELECT invoice_number as id, client_name_id , round(avg(round(julianday('now')-julianday(sale_date)))) as avg ,sum((total_amount-amount_paid)) as b
									FROM data_sale 
									WHERE created_by_id = '{0}' AND (sale_date BETWEEN '{1}' AND '{2}') AND (total_amount-amount_paid)>0 group by client_name_id order by client_name_id
									'''.format(user_id,first_date,last_date, )
								)


			payload = {'report':res2,'report2':res3 , 'username':username, 'firstdate':first_date, 'lastdate':last_date,}
			return render(request,'report/outstanding_report.html',payload)
		else:
			payload['form'] = OutstandingReport()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = OutstandingReport()
	
	return render(request,'report/report_form.html',payload)

@login_required(login_url='/login/')
def payment_register(request):
	payload = {}

	if request.method == 'POST':
		form = PaymentRegister(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_date = form.cleaned_data['start_date']
			last_date = form.cleaned_data['end_date']

			user_id = (User.objects.filter(username=username).first()).id

			# using RAW SQL in django
			
			res2 = Sample.objects.raw('''SELECT data_payment.id, data_payment.invoice_number_id ,data_sale.client_name_id , data_payment.date, data_sale.sale_date , round(julianday(data_payment.date)-julianday(data_sale.sale_date)) as diff , data_payment.amount_received as b
									FROM data_payment join data_sale on data_sale.invoice_number=data_payment.invoice_number_id
									WHERE data_payment.created_by_id = '{0}' AND (data_payment.date BETWEEN '{1}' AND '{2}') order by data_payment.date
									'''.format(user_id,first_date,last_date,)
								)

			res3 = Sample.objects.raw('''SELECT data_payment.id, data_sale.client_name_id , round(avg(round(julianday(data_payment.date)-julianday(data_sale.sale_date)))) as avg ,sum(data_payment.amount_received) as b
									FROM data_payment join data_sale on data_sale.invoice_number=data_payment.invoice_number_id
									WHERE data_payment.created_by_id = '{0}' AND (data_payment.date BETWEEN '{1}' AND '{2}') group by data_sale.client_name_id order by data_sale.client_name_id
									'''.format(user_id,first_date,last_date, )
								)


			payload = {'report':res2 ,'report2':res3 ,'username':username, 'firstdate':first_date, 'lastdate':last_date,}
			return render(request,'report/payment_register.html',payload)
		else:
			payload['form'] = PaymentRegister()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = PaymentRegister()
	
	return render(request,'report/report_form.html',payload)


@login_required(login_url='/login/')
def daily_sales(request):
	payload = {}

	if request.method == 'POST':
		form = DailySales(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_date = form.cleaned_data['start_date']
			last_date = form.cleaned_data['end_date']

			user_id = (User.objects.filter(username=username).first()).id

			# using RAW SQL in django
			res = Dsr.objects.raw('''SELECT data_dsr.id, data_dsr.client_name_id, data_dsr.contact_person, data_dsr.telephone, data_dsr.client_rank, data_dsr.contact_mode, data_dsr.date_of_contact, data_dsr.action, data_dsr.product_name_id, data_dsr.next_call_date 
			            			FROM data_dsr 
									WHERE data_dsr.created_by_id = '{0}' AND (data_dsr.date_of_contact BETWEEN '{1}' AND '{2}')
									'''.format(user_id,first_date,last_date)
								)

			payload = {'report':res, 'username':username, 'firstdate':first_date, 'lastdate':last_date}
			return render(request,'report/daily_sales.html',payload)
		else:
			payload['form'] = DailySales()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = DailySales()
	
	return render(request,'report/report_form.html',payload)

