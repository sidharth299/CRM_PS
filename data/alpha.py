# import csv
# from django.http import HttpResponse
from django.forms import TextInput, Textarea
from django.contrib import admin
from .dbconf import *

class DsrAdmin(admin.ModelAdmin):
	raw_id_fields = ('client_name',)
	readonly_fields = ('created_by',)

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super(DsrAdmin, self).save_model(request, obj, form, change)

class BillInline(admin.TabularInline):

	model = Bill
	extra = 1
	readonly_fields = ()

class SaleAdmin(admin.ModelAdmin):
	readonly_fields = ('amount_paid','first_date','last_date','created_by')
	inlines = [BillInline]

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super(SaleAdmin, self).save_model(request, obj, form, change)

class PaymentAdmin(admin.ModelAdmin):
	pass

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
	def object_link(self, obj):
	    if obj.action_flag == DELETION:
	        link = escape(obj.object_repr)
	    else:
	        ct = obj.content_type
	        link = u'<a href="%s">%s</a>' % (
	            reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
	            escape(obj.object_repr),
	        )
	    return link
	object_link.allow_tags = True
	object_link.admin_order_field = 'object_repr'
	object_link.short_description = u'object'
	"""
