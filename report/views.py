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
			user_id = (User.objects.filter(username=username).first()).id
			first_date = form.cleaned_data['start_date']
			last_date = form.cleaned_data['end_date']

			# count is referred as calls here
			# 1 visit -> 1 call
			# other mode of communication ->

			# using RAW SQL in django
			res = Dsr.objects.raw('''SELECT  id,date_of_contact,
									SUM(CASE WHEN contact_mode in ('Visit','Email','WhatsApp') THEN 3
											WHEN contact_mode = 'Telephone' THEN 1
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