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

			num=0
			calls=0

			for r in res:
				r.count = round(r.count/3,2)
				calls=calls+r.count
				num=num+1
			
			if num!=0:
				calls= round((calls/num),2)

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="LineChart.csv"'

				writer = csv.writer(response)
				# adding headres
				writer.writerow(['Date of Contact','Number of Calls'])
				for r in res:
					writer.writerow([r.date_of_contact,r.count])
				return response


			payload = {'report':res,'username':username, 'average':calls}
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
			is_csv = form.cleaned_data['is_csv']

			user_id = (User.objects.filter(username=username).first()).id

			# using RAW SQL in django
			res = Sample.objects.raw('''SELECT  data_sample.id, sent_date, data_client.client_name as client, data_sample.city, data_product.product_name as product, data_sample.sample_quantity, data_sample.sample_status, data_sample.remarks
									FROM data_sample join data_product on data_product.product_name=data_sample.product_name_id join data_client on data_client.client_name = data_sample.client_name_id
									WHERE data_sample.created_by_id = '{0}' AND (sent_date BETWEEN '{1}' AND '{2}') order by sent_date
									'''.format(user_id,first_date,last_date)
								)


			res2 = Sample.objects.raw('''SELECT  id, sample_status, count(id) as count
									FROM data_sample
									WHERE created_by_id = '{0}' AND (sent_date BETWEEN '{1}' AND '{2}') group by sample_status
									'''.format(user_id,first_date,last_date)
								)

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="SampleReport.csv"'

				writer = csv.writer(response)
				# adding headres
				writer.writerow(['Sent Date','Client Name','City','Product Name', 'Quantity', 'Status', 'Remarks' ])
				for r in res:
					writer.writerow([r.sent_date,r.client, r.city,  r.product, r.sample_quantity, r.sample_status, r.remarks ])
				return response


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
			is_csv = form.cleaned_data['is_csv']

			res = Client.objects.raw('''SELECT  client_name, client_category, city , telephone_main, client_rank from data_client where
										client_rank='{0}' order by client_name
									'''.format(rank,)
								)
			
			res2 = Client.objects.raw('''SELECT  client_name, count(client_name) as count from data_client where
										client_rank='{0}' order by client_name
									'''.format(rank,)
								)

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="RankRegister.csv"'

				writer = csv.writer(response)
				# adding headres
				writer.writerow(['Name','Category','City','Phone', 'Rank' ])
				for r in res:
					writer.writerow([r.client_name ,r.client_category, r.city,  r.telephone_main , r.client_rank ])
				return response


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
			is_csv = form.cleaned_data['is_csv']

			user_id = (User.objects.filter(username=username).first()).id

			# using RAW SQL in django
			res = Sale.objects.raw('''SELECT invoice_number,sale_date,client_name_id,client_category, SUM(total_amount) AS total
									FROM data_sale 
									JOIN data_client ON data_sale.client_name_id = data_client.client_name
									WHERE data_sale.created_by_id = '{0}' AND (sale_date BETWEEN '{1}' AND '{2}') GROUP BY client_name ORDER BY client_category, total desc
									'''.format(user_id,first_date,last_date)
								)	
			
			

			res2 = Sale.objects.raw('''SELECT invoice_number,client_category, SUM(total_amount) AS total
									FROM data_sale JOIN data_client ON data_sale.client_name_id = data_client.client_name
									WHERE data_sale.created_by_id = '{0}' AND (sale_date BETWEEN '{1}' AND '{2}')
									GROUP BY client_category ORDER BY SUM(total_amount)
									'''.format(user_id,first_date,last_date)
								)
			
			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="IndustrySales.csv"'

				writer = csv.writer(response)
				# adding headres
				writer.writerow(['Industry Type','Client name','Sum' ])
				for r in res:
					writer.writerow([r.client_category, r.client_name , r.total])
				return response
			
			
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
			is_csv = form.cleaned_data['is_csv']


			user_id = (User.objects.filter(username=username).first()).id

			# using RAW SQL in django
			res = Sample.objects.raw('''SELECT  data_bill.id, data_bill.product_name_id as p, sum(data_bill.quantity) as q, sum(data_bill.basic_rate*data_bill.quantity) as t
									FROM data_bill join data_sale on data_sale.invoice_number=data_bill.invoice_number_id
									WHERE data_sale.created_by_id = '{0}' AND (data_sale.sale_date BETWEEN '{1}' AND '{2}') group by data_bill.product_name_id order by t desc
									'''.format(user_id,first_date,last_date)
								)

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="ItemSales.csv"'

				writer = csv.writer(response)
				# adding headres
				writer.writerow(['Product','Quantity','Amount' ])
				for r in res:
					writer.writerow([r.p, r.q , r.t])
				return response

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
			is_csv = form.cleaned_data['is_csv']

			user_id = (User.objects.filter(username=username).first()).id

			

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

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="OutstandingReport.csv"'

				writer = csv.writer(response)
				# adding headres
				writer.writerow(['INVOICE','CLIENT NAME','DATE','OUTSTANDING DAYS','REMAINING PAYMENT' ])
				for r in res2:
					writer.writerow([r.id, r.client_name_id , r.sale_date, r.diff,r.b])
				return response


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
			is_csv = form.cleaned_data['is_csv']

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

			tot=0

			for r in res3:
				tot=tot+r.b

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="PaymentRegister.csv"'

				writer = csv.writer(response)
				# adding headres
				writer.writerow(['INVOICE','CLIENT NAME','SALE DATE','PAYMENT DATE','DAYS TO PAYMENT','PAYMENT RECEIVED' ])
				for r in res2:
					writer.writerow([r.invoice_number_id, r.client_name_id , r.sale_date,r.date, r.diff,r.b])
				return response


			payload = {'report':res2 ,'report2':res3 ,'username':username, 'firstdate':first_date, 'lastdate':last_date,'total':tot}
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
			is_csv = form.cleaned_data['is_csv']

			user_id = (User.objects.filter(username=username).first()).id

			# using RAW SQL in django
			res = Dsr.objects.raw('''SELECT data_dsr.id, data_dsr.client_name_id, data_dsr.contact_person, data_dsr.telephone, data_dsr.client_rank, data_dsr.contact_mode, data_dsr.date_of_contact, data_dsr.action, data_dsr.product_name_id, data_dsr.next_call_date 
			            			FROM data_dsr 
									WHERE data_dsr.created_by_id = '{0}' AND (data_dsr.date_of_contact BETWEEN '{1}' AND '{2}')
									'''.format(user_id,first_date,last_date)
								)

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="PaymentRegister.csv"'

				writer = csv.writer(response)
				# adding headres
				writer.writerow(['NAME','CONTACT PERSON','PHONE','RANK','CONTACT MODE','DATE OF CONTACT','ACTION','PRODUCT NAME','NEXT CALL DATE' ])
				for r in res:
					writer.writerow([r.client_name_id ,r.contact_person,r.telephone,r.client_rank,r.contact_mode,r.date_of_contact,r.action,r.product_name_id,r.next_call_date])
				return response

			payload = {'report':res, 'username':username, 'firstdate':first_date, 'lastdate':last_date}
			return render(request,'report/daily_sales.html',payload)
		else:
			payload['form'] = DailySales()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = DailySales()
	
	return render(request,'report/report_form.html',payload)


@login_required(login_url='/login/')
def perf_report(request):
	payload = {}

	if request.method == 'POST':
		form = PerfReport(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			first_date = form.cleaned_data['start_date']
			last_date = form.cleaned_data['end_date']
			is_csv = form.cleaned_data['is_csv']

			user_id = (User.objects.filter(username=username).first()).id

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

			calls=0
			num=0
			avg_calls=0

			for r in res:
				r.count = round(r.count/3,2)
				calls=calls+r.count
				num=num+1

			calls=round(calls,2)
			if num!=0:
				avg_calls=round((calls/num),2)

			res = Dsr.objects.raw('''SELECT  id, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{1}' AND '{2}') and entry_type='dealer_appointment'
									'''.format(user_id,first_date,last_date)
								)
			d_app=0

			for r in res:
				d_app=r.c

			res = Dsr.objects.raw('''SELECT  id, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{1}' AND '{2}') and entry_type='a_letter'
									'''.format(user_id,first_date,last_date)
								)

			a_letter=0

			for r in res:
				a_letter=r.c

			res = Dsr.objects.raw('''SELECT  id, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{1}' AND '{2}') and entry_type='big'
									'''.format(user_id,first_date,last_date)
								)

			big=0

			for r in res:
				big=r.c

			res = Dsr.objects.raw('''SELECT  id, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{1}' AND '{2}') and entry_type='converted'
									'''.format(user_id,first_date,last_date)
								)

			conv=0
			hit_ratio=0
			for r in res:
				conv=r.c

			if conv!=0:
				hit_ratio=round((calls/conv),2)

			res = Dsr.objects.raw('''SELECT  id, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{1}' AND '{2}') and entry_type='repeat'
									'''.format(user_id,first_date,last_date)
								)

			repeat=0

			for r in res:
				repeat=r.c

			res = Sample.objects.raw('''SELECT data_payment.id, data_sale.client_name_id , round(avg(round(julianday(data_payment.date)-julianday(data_sale.sale_date)))) as avg ,sum(data_payment.amount_received) as b
									FROM data_payment join data_sale on data_sale.invoice_number=data_payment.invoice_number_id
									WHERE data_payment.created_by_id = '{0}' AND (data_payment.date BETWEEN '{1}' AND '{2}') group by data_sale.client_name_id order by data_sale.client_name_id
									'''.format(user_id,first_date,last_date, )
								)

			p_tot=0

			for r in res:
				p_tot=p_tot+r.b

			res = Sample.objects.raw('''SELECT invoice_number as id, client_name_id , sale_date, round(julianday('now')-julianday(sale_date)) as diff , sum(total_amount) as b
									FROM data_sale 
									WHERE created_by_id = '{0}' AND (sale_date BETWEEN '{1}' AND '{2}')
									'''.format(user_id,first_date,last_date,)
								)
	
			s_tot=0
			num_invoice=0

			for r in res:
				if r.b!=None:
					s_tot=s_tot+r.b
				
			res = Sample.objects.raw('''SELECT invoice_number as id, client_name_id , sale_date, total_amount as b
									FROM data_sale 
									WHERE created_by_id = '{0}' AND (sale_date BETWEEN '{1}' AND '{2}')
									'''.format(user_id,first_date,last_date,)
								)

			for r in res:
				num_invoice=num_invoice+1

			ats=0

			if num_invoice!=0:
				ats=round((s_tot/num_invoice),2)

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="PerformanceReport.csv"'

				writer = csv.writer(response)
				csv_calls=['Total Calls']
				csv_mnoc=['MNOC']
				csv_dappt=['Dealer Appointments']
				csv_aletter=["Appreciation Letter"]
				csv_big=["Big"]
				csv_conv=["Converted"]
				csv_hit=["HIT ratio"]
				csv_repeat=["Repeat"]
				csv_sale=["Sales"]
				csv_payment=["Collection"]
				csv_invoice=["No. of invoices generated"]
				csv_ats=["ATS"]

				csv_calls.append(calls)
				csv_mnoc.append(avg_calls)
				csv_dappt.append(d_app)
				csv_aletter.append(a_letter)
				csv_big.append(big)
				csv_conv.append(conv)
				csv_hit.append(hit_ratio)
				csv_repeat.append(repeat)
				csv_sale.append(s_tot)
				csv_payment.append(p_tot)
				csv_invoice.append(num_invoice)	
				csv_ats.append(ats)
					


				# adding headres
				writer.writerow(["Performance Report"])
				writer.writerow(['Metric','Achieved' ])
				writer.writerow(csv_calls)
				writer.writerow(csv_mnoc)
				writer.writerow(csv_dappt)
				writer.writerow(csv_aletter)
				writer.writerow(csv_big)
				writer.writerow(csv_conv)
				writer.writerow(csv_hit)
				writer.writerow(csv_repeat)
				writer.writerow(csv_sale)
				writer.writerow(csv_payment)
				writer.writerow(csv_invoice)
				writer.writerow(csv_ats)

				return response

			payload = {'username':username, 'firstdate':first_date, 'lastdate':last_date, 'calls':calls,'avg_calls':avg_calls ,'d_app':d_app, 'a_letter':a_letter, 'big':big, 'conv':conv, 'hit_ratio':hit_ratio, 'repeat':repeat, 'p_total':p_tot, 's_total':s_tot, 'num_invoice':num_invoice, 'ats':ats}
			return render(request,'report/perf_report.html',payload)
		else:
			payload['form'] = PerfReport()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = PerfReport()
	
	return render(request,'report/report_form.html',payload)

@login_required(login_url='/login/')
def strategic_report(request):
	payload = {}

	if request.method == 'POST':
		form = StrategicReport(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			year1 = form.cleaned_data['year']
			is_csv = form.cleaned_data['is_csv']
			year2=year1+1
			user_id = (User.objects.filter(username=username).first()).id


			d_appointment=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			for i in range(1,13):
				if i<10:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='dealer_appointment' and strftime('%m',entry_date)='0{1}'
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='dealer_appointment' and strftime('%m',entry_date)='{1}'
									'''.format(user_id, i, year1, year2)
								)
				d_app=0
				for r in res:
					d_app=r.c
				if i<4:
					d_appointment[i+8]=d_app
				else:
					d_appointment[i-4]=d_app

			for i in range(12):
				d_appointment[12]+=d_appointment[i]

			target_da=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_al=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_big=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_conv=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_ref=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_cross=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_repeat=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_sale=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_ats=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_pay=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_hit=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_total_call=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_avg_call=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			target_invoice=[0,0,0,0,0,0,0,0,0,0,0,0,0]



			res = Target.objects.raw('''SELECT id, d_appointment ,appr_letter,big,ref_sale,cross_sale,rank_6_7,MTD_sales,ats,MTD_collection,hit_ratio, mnoc, lead_gen
									FROM data_target
									WHERE user_id_id = '{0}'
									'''.format(user_id,)
								)


			
				
			tar_da=0
			tar_al=0
			tar_big=0
			tar_ref=0
			tar_cross=0
			tar_repeat=0
			tar_sale=0
			tar_ats=0
			tar_pay=0
			tar_hit=0
			tar_mnoc=0
			tar_conv=0
			i=0
			for r in res:
				tar_da=r.d_appointment
				tar_al=r.appr_letter
				tar_big=r.big
				tar_ref=r.ref_sale
				tar_cross=r.cross_sale
				tar_repeat=r.rank_6_7
				tar_sale=r.MTD_sales
				tar_ats=r.ats
				tar_pay=r.MTD_collection
				tar_hit=r.hit_ratio
				tar_mnoc=r.mnoc
				tar_conv=r.lead_gen
			
				target_da[i]=tar_da
				target_al[i]=tar_al
				target_big[i]=tar_big
				target_ref[i]=tar_ref
				target_cross[i]=tar_cross
				target_repeat[i]=tar_repeat
				target_sale[i]=tar_sale
				target_ats[i]=tar_ats
				target_pay[i]=tar_pay
				target_hit[i]=tar_hit
				target_conv[i]=tar_conv
				target_avg_call[i]=tar_mnoc

				i=i+1

			
			for i in range(12):
				target_da[12]+=target_da[i]
				target_al[12]+=target_al[i]
				target_big[12]+=target_big[i]
				target_ref[12]+=target_ref[i]
				target_cross[12]+=target_cross[i]
				target_repeat[12]+=target_repeat[i]
				target_sale[12]+=target_sale[i]
				target_ats[12]+=target_ats[i]
				target_pay[12]+=target_pay[i]
				target_hit[12]+=target_hit[i]
				target_conv[12]+=target_conv[i]
				target_avg_call[12]+=target_avg_call[i]

			target_hit[12]=round((target_hit[12]/12),2)
			target_ats[12]=round((target_ats[12]/12),2)
			target_avg_call[12]=round((target_avg_call[12]/12),2)

			a_letter_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			for i in range(1,13):
				if i<10:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='a_letter' and strftime('%m',entry_date)='0{1}'
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='a_letter' and strftime('%m',entry_date)='{1}'
									'''.format(user_id, i, year1, year2)
								)
				a_letter=0
				for r in res:
					a_letter=r.c
				if i<4:
					a_letter_list[i+8]=a_letter
				else:
					a_letter_list[i-4]=a_letter

			for i in range(12):
				a_letter_list[12]+=a_letter_list[i]

			big_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			for i in range(1,13):
				if i<10:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='big' and strftime('%m',entry_date)='0{1}'
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='big' and strftime('%m',entry_date)='{1}'
									'''.format(user_id, i, year1, year2)
								)
				big=0
				for r in res:
					big=r.c
				if i<4:
					big_list[i+8]=big
				else:
					big_list[i-4]=big

			for i in range(12):
				big_list[12]+=big_list[i]

			conv_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			for i in range(1,13):
				if i<10:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='converted' and strftime('%m',entry_date)='0{1}'
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='converted' and strftime('%m',entry_date)='{1}'
									'''.format(user_id, i, year1, year2)
								)
				conv=0
				for r in res:
					conv=r.c
				if i<4:
					conv_list[i+8]=conv
				else:
					conv_list[i-4]=conv

			for i in range(12):
				conv_list[12]+=conv_list[i]
			
			ref_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			for i in range(1,13):
				if i<10:
					res = Sale.objects.raw('''SELECT  invoice_number, strftime('%m',sale_date) as m, count(invoice_number) as c
									FROM data_sale JOIN data_client ON client_name=client_name_id
									WHERE data_sale.created_by_id = '{0}' AND (sale_date BETWEEN '{2}-04-01' AND '{3}-03-31') and lead_source='Reference' and strftime('%m',sale_date)='0{1}'
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Sale.objects.raw('''SELECT  invoice_number, strftime('%m',sale_date) as m, count(invoice_number) as c
									FROM data_sale JOIN data_client ON client_name=client_name_id
									WHERE data_sale.created_by_id = '{0}' AND (sale_date BETWEEN '{2}-04-01' AND '{3}-03-31') and lead_source='Reference' and strftime('%m',sale_date)='{1}'
									'''.format(user_id, i, year1, year2)
								)
				ref=0
				for r in res:
					ref=r.c
				if i<4:
					ref_list[i+8]=ref
				else:
					ref_list[i-4]=ref

			for i in range(12):
				ref_list[12]+=ref_list[i]

			cross_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			for i in range(1,13):
				if i<10:
					res = Sale.objects.raw('''SELECT  invoice_number, strftime('%m',sale_date) as m, count(invoice_number) as c
									FROM data_sale 
									WHERE data_sale.created_by_id = '{0}' AND (sale_date BETWEEN '{2}-04-01' AND '{3}-03-31') and remarks='CROSS' and strftime('%m',sale_date)='0{1}'
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Sale.objects.raw('''SELECT  invoice_number, strftime('%m',sale_date) as m, count(invoice_number) as c
									FROM data_sale 
									WHERE data_sale.created_by_id = '{0}' AND (sale_date BETWEEN '{2}-04-01' AND '{3}-03-31') and remarks='CROSS' and strftime('%m',sale_date)='{1}'
									'''.format(user_id, i, year1, year2)
								)
				cross=0
				for r in res:
					cross=r.c
				if i<4:
					cross_list[i+8]=cross
				else:
					cross_list[i-4]=cross

			for i in range(12):
				cross_list[12]+=cross_list[i]


			repeat_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			for i in range(1,13):
				if i<10:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='repeat' and strftime('%m',entry_date)='0{1}'
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Dsr.objects.raw('''SELECT  id, strftime('%m',entry_date) as m, count(id) as c
									FROM data_entry
									WHERE user_id_id = '{0}' AND (entry_date BETWEEN '{2}-04-01' AND '{3}-03-31') and entry_type='repeat' and strftime('%m',entry_date)='{1}'
									'''.format(user_id, i, year1, year2)
								)
				repeat=0
				for r in res:
					repeat=r.c
				if i<4:
					repeat_list[i+8]=repeat
				else:
					repeat_list[i-4]=repeat

			for i in range(12):
				repeat_list[12]+=repeat_list[i]

			sale_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			invoices_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			for i in range(1,13):
				if i<10:
					res = Dsr.objects.raw('''SELECT invoice_number as id, total_amount as b
									FROM data_sale 
									WHERE created_by_id = '{0}' AND (sale_date BETWEEN '{2}-04-01' AND '{3}-03-31') and strftime('%m',sale_date)='0{1}'
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Dsr.objects.raw('''SELECT invoice_number as id, total_amount as b
									FROM data_sale 
									WHERE created_by_id = '{0}' AND (sale_date BETWEEN '{2}-04-01' AND '{3}-03-31') and strftime('%m',sale_date)='{1}'
									'''.format(user_id, i, year1, year2)
								)
				
				s_tot=0
				num_invoice=0
				for r in res:
					s_tot=s_tot+r.b
					num_invoice=num_invoice+1
				if i<4:
					sale_list[i+8]=s_tot
					invoices_list[i+8]=num_invoice
				else:
					sale_list[i-4]=s_tot
					invoices_list[i-4]=num_invoice

			for i in range(12):
				sale_list[12]=sale_list[12]+sale_list[i]
				invoices_list[12]=invoices_list[12]+invoices_list[i]

			ats_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			for i in range(12):
				if invoices_list[i]==0:
					continue
				ats_list[i]=round((sale_list[i]/invoices_list[i]),2)

			if invoices_list[12]!=0:
				ats_list[12]=round((sale_list[12]/invoices_list[12]),2)


			payment_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			for i in range(1,13):
				if i<10:
					res = Dsr.objects.raw('''SELECT data_payment.id, data_payment.amount_received as b
									FROM data_payment
									WHERE created_by_id = '{0}' AND (date BETWEEN '{2}-04-01' AND '{3}-03-31') and strftime('%m',date)='0{1}'
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Dsr.objects.raw('''SELECT data_payment.id, data_payment.amount_received as b
									FROM data_payment
									WHERE created_by_id = '{0}' AND (date BETWEEN '{2}-04-01' AND '{3}-03-31') and strftime('%m',date)='{1}'
									'''.format(user_id, i, year1, year2)
								)
				p_tot=0
				for r in res:
					p_tot=p_tot+r.b
				if i<4:
					payment_list[i+8]=p_tot
				else:
					payment_list[i-4]=p_tot

			for i in range(12):
				payment_list[12]=payment_list[12]+payment_list[i]


			total_call_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			avg_call_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]

			num_avg=0
			for i in range(1,13):
				if i<10:
					res = Dsr.objects.raw('''SELECT  id,date_of_contact ,
									SUM(CASE WHEN contact_mode = 'Visit' THEN 3
											WHEN contact_mode in ('Telephone','Email','WhatsApp') THEN 1
											ELSE 0 END) 
									AS count 
									FROM data_dsr
									WHERE created_by_id = '{0}' AND (date_of_contact BETWEEN '{2}-04-01' AND '{3}-03-31') and strftime('%m',date_of_contact)='0{1}' group by date_of_contact
									'''.format(user_id, i, year1, year2)
								)
				else:
					res = Dsr.objects.raw('''SELECT  id,date_of_contact ,
									SUM(CASE WHEN contact_mode = 'Visit' THEN 3
											WHEN contact_mode in ('Telephone','Email','WhatsApp') THEN 1
											ELSE 0 END) 
									AS count 
									FROM data_dsr
									WHERE created_by_id = '{0}' AND (date_of_contact BETWEEN '{2}-04-01' AND '{3}-03-31') and strftime('%m',date_of_contact)='{1}' group by date_of_contact
									'''.format(user_id, i, year1, year2)
								)
				calls=0
				num=0
				avg_calls=0
				for r in res:
					r.count = round(r.count/3,2)
					calls=calls+r.count
					num=num+1

				num_avg+=num

				calls=round(calls,2)
				if num!=0:
					avg_calls=round((calls/num),2)
			
				if i<4:
					total_call_list[i+8]=calls
					avg_call_list[i+8]=avg_calls
				else:
					total_call_list[i-4]=calls
					avg_call_list[i-4]=avg_calls

			for i in range(12):
				total_call_list[12]+=total_call_list[i]

			total_call_list[12]=round(total_call_list[12],2)

			if num_avg!=0:
				avg_call_list[12]=round((total_call_list[12]/num_avg),2)

			hit_ratio_list=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			for i in range(12):
				if conv_list[i]==0:
					continue
				hit_ratio_list[i]=round((total_call_list[i]/conv_list[i]),2)

			if conv_list[12]!=0:
				hit_ratio_list[12]=round((total_call_list[12]/conv_list[12]),2)

			if is_csv:
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="StrategicReport.csv"'

				writer = csv.writer(response)

				csv_mnoc=['MNOC']
				csv_dappt=['Dealer Appointments']
				csv_aletter=["Appreciation Letter"]
				csv_big=["Big"]
				csv_conv=["Converted"]
				csv_ref=["Reference"]
				csv_cross=["Cross"]
				csv_hit=["HIT ratio"]
				csv_repeat=["Repeat"]
				csv_sale=["Sales"]
				csv_payment=["Collection"]
				csv_ats=["ATS"]

				for i in range(13):
					csv_mnoc.append(target_avg_call[i])
					csv_mnoc.append(avg_call_list[i])

					csv_dappt.append(target_da[i])
					csv_dappt.append(d_appointment[i])

					csv_aletter.append(target_al[i])
					csv_aletter.append(a_letter_list[i])

					csv_big.append(target_big[i])
					csv_big.append(big_list[i])

					csv_conv.append(target_conv[i])
					csv_conv.append(conv_list[i])

					csv_ref.append(target_ref[i])
					csv_ref.append(ref_list[i])

					csv_cross.append(target_cross[i])
					csv_cross.append(cross_list[i])

					csv_hit.append(target_hit[i])
					csv_hit.append(hit_ratio_list[i])

					csv_repeat.append(target_repeat[i])
					csv_repeat.append(repeat_list[i])

					csv_sale.append(target_sale[i])
					csv_sale.append(sale_list[i])

					csv_payment.append(target_pay[i])
					csv_payment.append(payment_list[i])

					csv_ats.append(target_ats[i])
					csv_ats.append(ats_list[i])
					


				# adding headres
				writer.writerow(["Strategic Report"])
				writer.writerow(['Metric','April','','May','','June','','July','','August','','September','','October','' ,'November','', 'December','', 'January','','February','','March','', 'Total','' ])
				writer.writerow(['','T','A','T','A','T','A','T','A','T','A','T','A','T','A' ,'T','A', 'T','A', 'T','A','T','A','T','A', 'T','A' ])
				writer.writerow(csv_mnoc)
				writer.writerow(csv_dappt)
				writer.writerow(csv_aletter)
				writer.writerow(csv_big)
				writer.writerow(csv_conv)
				writer.writerow(csv_ref)
				writer.writerow(csv_cross)
				writer.writerow(csv_hit)
				writer.writerow(csv_repeat)
				writer.writerow(csv_sale)
				writer.writerow(csv_payment)
				writer.writerow(csv_ats)

				return response

			payload = {'username':username,'year1':year1,'year2':year2  ,'d_appointment':d_appointment, 'target_da':target_da,'target_al':target_al,'target_big':target_big,'target_invoice':target_invoice,'target_ref':target_ref,'target_cross':target_cross,'target_conv':target_conv,'target_repeat':target_repeat,'target_sale':target_sale,'target_ats':target_ats,'target_pay':target_pay,'target_hit':target_hit,'target_total_call':target_total_call,'target_avg_call':target_avg_call, 'a_letter':a_letter_list, 'big':big_list, 'conv':conv_list, 'ref':ref_list, 'cross':cross_list, 'repeat':repeat_list, 'sales':sale_list, 'invoices':invoices_list, 'ats':ats_list, 'payment':payment_list, 't_calls':total_call_list, 'avg_calls':avg_call_list, 'hit_ratio': hit_ratio_list}
			return render(request,'report/strategic_report.html',payload)
		else:
			payload['form'] = StrategicReport()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = StrategicReport()
	
	return render(request,'report/report_form.html',payload)