from django import forms

from django.contrib.auth.models import User
from data.models import *
import datetime
def present_or_past_date(value):
    if value > datetime.date.today():
        raise forms.ValidationError("The date cannot be in the future!")
    return value


class LineChart(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')
	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date])
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date])
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class SampleReport(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')
	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)



class RankRegister(forms.Form):
	rank= forms.IntegerField(max_value=7, min_value=1)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class IndustrySales(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')
	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date],
								required = True)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date],
								required = True)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class ItemSales(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class OutstandingReport(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class PaymentRegister(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class DailySales(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class PerfReport(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),validators=[present_or_past_date]
								)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

class StrategicReport(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')

	year= forms.IntegerField(max_value=2050, min_value=2000,initial=2019)
	is_csv     = forms.BooleanField(help_text='Download the report as CSV', required=False)

