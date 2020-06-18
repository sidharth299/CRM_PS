from django.contrib import admin

from .models import *

class AdvanceInvoiceListFilter(admin.SimpleListFilter):
    title = 'Invoice Type'
    parameter_name = 'invoice'

    def lookups(self, request, model_admin):

        return (
            ('advance','Advance'),
            ('nonadvance', 'Non Advance'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'advance':
            return queryset.filter(total_amount=0,amount_paid__gte=0)
        if self.value() == 'nonadvance':
            return queryset.filter(total_amount__gt=0)
