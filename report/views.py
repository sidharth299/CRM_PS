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
			res = Sample.objects.raw('''SELECT  id, sent_date, client_id_id, city, product_id_id, sample_quantity, sample_status
									FROM data_sample
									WHERE created_by_id = '{0}' AND (sent_date BETWEEN '{1}' AND '{2}') order by sent_date
									'''.format(user_id,first_date,last_date)
								)

			payload = {'report':res,'username':username}
			return render(request,'report/sample_report.html',payload)
		else:
			payload['form'] = LineChart()
			return render(request,'report/report_form.html',payload)

	else:
		payload['form'] = LineChart()
	
	return render(request,'report/report_form.html',payload)