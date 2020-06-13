# used creating a form from a Model
# from django.forms import ModelForm
# creating a normal form
from django import forms

from django.contrib.auth.models import User
from data.models import *

class LineChart(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')
	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								required = True)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								required = True)

class SampleReport(forms.Form):
	username = forms.ModelChoiceField(
									queryset=User.objects.all().order_by('username'),
									help_text='select the username')
	start_date = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								required = True)
	end_date   = forms.DateField(
								widget=forms.widgets.DateInput(attrs={'type': 'date'}),
								required = True)

class RankRegister(forms.Form):
	rank= forms.IntegerField(max_value=7, min_value=1)


"""
# an example of how to generate forms from model
class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ("username",)
"""