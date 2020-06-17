from django import forms

from django.contrib.auth.models import User
from data.models import *

class LineChart(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')
	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}))
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}))
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class SampleReport(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')
	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)



class RankRegister(forms.Form):
	rank= forms.IntegerField(max_value=7, min_value=1)

class IndustrySales(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')
	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								required = True)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								required = True)
class ItemSales(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class OutstandingReport(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class PaymentRegister(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class DailySales(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class PerfReport(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)