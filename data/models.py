from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

from .constants import *

# has to have add some of the null=True only for the time being will fix it when backend will be populating the data instead
# remove null from all places WHERE NOT required

def get_financial_year():
    temp = datetime.now()
    month = temp.month
    if month in [1,2,3]:
        year = temp.year-1
    else:
        year = temp.year
    next_year = str(year+1)
    res = str(year)+'-'+next_year[-2:]
    return res

def get_invoice_number():
    invoice = Sale.objects.all().last()
    reset = False
    financial_year = get_financial_year()
    if invoice == None:
        reset = True
    else:
        temp = (invoice.invoice_number).split('~')
        year = temp[1]
        if year == financial_year:
            res = int(temp[0])+1
        else:
            reset = True
    if reset:
        res = 1

    response = str(res)+'~'+financial_year

    return response

# add/changed by only admin
class Product(models.Model):
    product_name     = models.CharField(max_length = MAX_PRODUCT_NAME, primary_key=True, verbose_name = "Product Name")
    product_category = models.CharField(choices = CHOICES_PRODUCT_CATEGORY, max_length = MAX_PRODUCT_CATEGORY, verbose_name = "Product Type")
    # REMOVE NULL from hsn_code
    hsn_code         = models.PositiveIntegerField(null=True, verbose_name = "HSN Code")
    basic_rate       = models.PositiveIntegerField(verbose_name = "Basic Cost")
    tax_rate         = models.DecimalField(default=18.00,decimal_places = 2, max_digits = 4, verbose_name = "Tax Rate")
    export_tax_rate  = models.DecimalField(default=0.1,decimal_places = 2, max_digits = 4, verbose_name = "Export Tax Rate")
    remarks          = models.CharField(blank = True, max_length = MAX_REMARKS, verbose_name = "Remarks")
    created_by       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT, verbose_name = "Created By")

    def __str__(self):
        return self.product_name

class Client(models.Model):

    client_name      = models.CharField(max_length = MAX_CLIENT_NAME, primary_key = True, verbose_name = "Client Name")
    gstin            = models.CharField(blank = True, max_length = 15, verbose_name = "GSTIN")
    client_category  = models.CharField(choices = CHOICES_CLIENT_CATEGORY, max_length = MAX_CLIENT_CATEGORY, verbose_name = "Client Category")
    btc              = models.CharField(blank = True, choices = CHOICES_BTC, max_length = MAX_BTC, verbose_name = "BTC Category")
    telephone_main   = models.CharField(blank = True, max_length = 15, verbose_name = "Telephone Number")
    telephone_extra  = models.CharField(blank = True, max_length = 15, verbose_name = "Telephone Number (Extra)")
    email            = models.EmailField(blank = True, verbose_name = "Email Address")
    contact_person   = models.CharField(blank = True, max_length = MAX_CONTACT_PERSON, verbose_name = "Contact Person Name")
    address          = models.CharField(blank = True, max_length = MAX_ADDRESS, verbose_name = "Office Address")
    city             = models.CharField(blank = True, max_length = MAX_CITY, verbose_name = "City")
    pin_code         = models.PositiveIntegerField(blank = True, null=True, validators=[MinValueValidator(100000), MaxValueValidator(999999)], verbose_name = "PIN Code")
    state            = models.CharField(blank = True, choices = CHOICES_STATE , default = DEFAULT_STATE, max_length = MAX_STATE, verbose_name = "State")
    country          = models.CharField(blank  = True, choices = CHOICES_COUNTRY, default = DEFAULT_COUNTRY, max_length = MAX_COUNTRY, verbose_name = "Country")
    zone             = models.CharField(blank=True , choices=CHOICES_ZONE, default= DEFAULT_ZONE, max_length=MAX_ZONE, verbose_name = "Zone")
    client_rank      = models.PositiveSmallIntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name = "Client Rank")
    lead_source      = models.CharField(choices = CHOICES_LEAD_SOURCE, default=DEFAULT_LEAD_SOURCE, max_length = MAX_LEAD_SOURCE, verbose_name = "Lead Source")
    remarks          = models.CharField(blank = True, max_length = MAX_REMARKS,verbose_name = "Remarks")
    balance          = models.IntegerField(default = 0, verbose_name = "Balance Amount Remaining")
    created_by       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT, verbose_name = "Created By")

    def __str__(self):
        return self.client_name

class Dsr(models.Model):

    client_name     = models.ForeignKey(Client, on_delete = models.PROTECT, verbose_name = "Client Name")
    contact_person  = models.CharField(blank = True, max_length = MAX_CONTACT_PERSON, verbose_name = "Contact Person")
    telephone       = models.CharField(blank = True, max_length = 15, verbose_name = "Telephone Number")
    email           = models.EmailField(blank = True, verbose_name = "Email Address")
    contact_mode    = models.CharField(choices = CHOICES_CONTACT_MODE, max_length = MAX_CONTACT_MODE,  verbose_name = "Contact Mode")
    date_of_contact = models.DateField(default = timezone.now,  verbose_name = "Date of Contact")
    action          = models.CharField(max_length = MAX_REMARKS,  verbose_name = "Action Taken")
    product_name    = models.ForeignKey(Product, blank = True, null = True,on_delete = models.PROTECT,  verbose_name = "Product Name")
    next_call_date  = models.DateField( verbose_name = "Next Call Date")
    sample_status   = models.CharField(blank = True, choices = CHOICES_SAMPLE_STATUS, max_length = MAX_SAMPLE_STATUS, verbose_name = "Sample Status")
    client_rank     = models.PositiveSmallIntegerField(default = 1, validators = [MinValueValidator(1), MaxValueValidator(7)], verbose_name = "Client Rank")
    failed_sale     = models.BooleanField(default = False, verbose_name = "Sale Failed")
    successful_sale = models.BooleanField(default = False, verbose_name = "Sale Successful")
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT, verbose_name = "Created By")

    def __str__(self):
        return self.action

class Sample(models.Model):

    client_name     = models.ForeignKey(Client, on_delete = models.PROTECT, verbose_name = "Client Name")
    sent_date       = models.DateField(default = timezone.now, verbose_name = "Sample Sent On")
    city            = models.CharField(blank = True, max_length = MAX_CITY, verbose_name = "City")
    product_name    = models.ForeignKey(Product, blank = True, null = True, on_delete = models.PROTECT, verbose_name = "Product Name")
    sample_quantity = models.PositiveIntegerField(verbose_name = "Quantity of Sample sent")
    sample_status   = models.CharField(choices = CHOICES_SAMPLE_STATUS, max_length = MAX_SAMPLE_STATUS, verbose_name = "Sample Status")
    remarks         = models.CharField(blank = True, max_length = MAX_REMARKS, verbose_name = "Remarks")
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT, verbose_name = "Created By")

    def __str__(self):
        return self.sample_status

# only Admin/Accountants
class Sale(models.Model):

    #invoice_number  = models.AutoField(primary_key = True, verbose_name = "Invoice Number")
    invoice_number  = models.CharField(default = get_invoice_number, max_length = MAX_INVOICE_NUMBER , primary_key = True, verbose_name = "Invoice Number")
    sale_date       = models.DateField(default = timezone.now, verbose_name = "Sale Date")
    client_name     = models.ForeignKey(Client, on_delete = models.PROTECT, verbose_name = "Client Name")
    carting         = models.PositiveIntegerField(default = 0, verbose_name = "Carting")
    gstin           = models.CharField(blank = True, max_length = 15, verbose_name = "GSTIN")
    tax_type        = models.CharField(choices = CHOICES_TAX_TYPE, max_length = MAX_TAX_TYPE, verbose_name = "Tax Type")
    igst            = models.DecimalField(decimal_places = 2, max_digits = 20, verbose_name = "IGST")
    cgst            = models.DecimalField(decimal_places = 2, max_digits = 20, verbose_name = "CGST")
    sgst            = models.DecimalField(decimal_places = 2, max_digits = 20, verbose_name = "SGST")
    export_sale     = models.DecimalField(decimal_places = 2, max_digits = 20, verbose_name = "Export Sale")
    total_amount    = models.PositiveIntegerField(verbose_name = "Total Amount")
    amount_paid     = models.PositiveIntegerField(default=0, verbose_name = "Amount Paid")
    first_date      = models.DateField(blank = True, null=True, verbose_name = "First Date of Payment")
    last_date       = models.DateField(blank = True , null=True, verbose_name = "Last Date of Payment")
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT, verbose_name = "Created By")
    remarks         = models.CharField(blank= True, max_length=10, verbose_name = "Remarks")

    def __str__(self):
        return str(self.client_name)+': Invoice No.'+str(self.invoice_number)

# not to be displayed to anyone
class Bill(models.Model):

    invoice_number  = models.ForeignKey(Sale, on_delete = models.CASCADE, verbose_name = "Invoice Number")
    product_name    = models.ForeignKey(Product, on_delete = models.PROTECT, verbose_name = "Product Name")
    # REMOVE null from basic rate
    basic_rate      = models.PositiveIntegerField(blank = True, null = True, verbose_name = "Basic Cost")
    quantity        = models.PositiveIntegerField(verbose_name = "Quantity Supplied")

    def __str__(self):
        return str(self.product_name)+' : '+str(self.quantity)

class Payment(models.Model):
    invoice_number  = models.ForeignKey(Sale, on_delete = models.CASCADE, verbose_name = "Invoice Number")
    date            = models.DateField(default = timezone.now, verbose_name = "Date")
    amount_received = models.PositiveIntegerField(verbose_name = "Amount Received")
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT, verbose_name = "Created By")

    def __str__(self):
        return str(self.invoice_number) + ' : Rs.' + str(self.amount_received)

"""
adding two new models
"""
class Target(models.Model):
    user_id           = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    period            = models.CharField(max_length = MAX_PERIOD)
    big               = models.IntegerField(default = 0)
    other             = models.IntegerField(default = 0)
    sale_value        = models.DecimalField(default=0, decimal_places = 2, max_digits = 10)
    lead_gen          = models.DecimalField(default=0, decimal_places = 2, max_digits = 10)
    mnoc              = models.DecimalField(default=0, decimal_places = 2, max_digits = 5)
    cross_sale        = models.IntegerField(default = 0)
    ref_sale          = models.IntegerField(default = 0)
    up_sale           = models.IntegerField(default = 0)
    lost_sale         = models.IntegerField(default = 0)
    rank_6_7          = models.IntegerField(default = 0)
    d_appointment     = models.IntegerField(default = 0)
    appr_letter       = models.IntegerField(default = 0)
    hit_ratio         = models.IntegerField(default = 0)
    ats               = models.DecimalField(default=0, decimal_places = 2, max_digits = 10)
    MTD_sales         = models.DecimalField(default=0, decimal_places = 2, max_digits = 10)
    total_outstanding = models.DecimalField(default=0, decimal_places = 2, max_digits = 10)
    MTD_collection    = models.DecimalField(default=0, decimal_places = 2, max_digits = 10)

    def __str__(self):
        return str(self.user_id)

class Entry(models.Model):
    user_id       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    entry_type  = models.CharField(choices = CHOICES_ENTRY_TYPE, max_length = MAX_ENTRY_TYPE)
    entry_date    = models.DateField(default = timezone.now)

    def __str__(self):
        return str(self.entry_type)

"""
    def publish(self):
        self.published_date = timezone.now()
        self.save()
"""
