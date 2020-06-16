# alpha has all classes except DsrAdmin and SampleAdmin
from .alpha import *
# beta has DsrAdmin and SampleAdmin
from .beta import *

# just comment the line of the model below you want to hide from the admin dashboard

"""
fieldsets
list_display = ('item_id', 'item_type', 'item_title', 'item_size', 'item_color',)
list_filter = ['']
search_fields = ('item_id', 'item_title',)
readonly_fields = ('disable_add_date','disable_remove_date',)
exclude = ('add_date', 'remove_date',)

-saleperson group
-verbose for two new models and check for all
"""

admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)

admin.site.register(Dsr, DsrAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Payment, PaymentAdmin)

# new models
admin.site.register(Target, TargetAdmin)
admin.site.register(Entry, EntryAdmin)