# alpha has all classes except DsrAdmin and SampleAdmin
from .alpha import *
# beta has DsrAdmin and SampleAdmin
from .beta import *

# just comment the line of the model below you want to hide from the admin dashboard

admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)

admin.site.register(Dsr, DsrAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Payment, PaymentAdmin)

# new models
admin.site.register(Target, TargetAdmin)
admin.site.register(Entry, EntryAdmin)