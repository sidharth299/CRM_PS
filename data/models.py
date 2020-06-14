from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import *

# has to have add some of the null=True only for the time being will fix it when backend will be populating the data instead

# add/changed by only admin
class Product(models.Model):
    product_name     = models.CharField(max_length = MAX_PRODUCT_NAME, primary_key=True, verbose_name = "Product Name")
    product_category = models.CharField(choices = CHOICES_PRODUCT_CATEGORY, max_length = MAX_PRODUCT_CATEGORY, verbose_name = "Product Type")
    hsn_code         = models.PositiveIntegerField(null=True, verbose_name = "HSN Code")
    basic_rate       = models.PositiveIntegerField(verbose_name = "Basic Cost")
    tax_rate         = models.DecimalField(decimal_places = 2, max_digits = 4, verbose_name = "Tax Rate")
    export_tax_rate  = models.DecimalField(decimal_places = 2, max_digits = 4, verbose_name = "Export Tax Rate")
    remarks          = models.CharField(blank = True, max_length = MAX_REMARKS, verbose_name = "Remarks")
    created_by       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name = "Created By")

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
    latest_dsr_id    = models.PositiveIntegerField(blank = True, null = True, verbose_name = "Latest DSR ID")
    created_by       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name = "Created By")


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
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name = "Created By")

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
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name = "Created By")

    def __str__(self):
        return str(self.sent_date)

# only Admin/Accountants
class Sale(models.Model):

    invoice_number  = models.AutoField(primary_key = True, verbose_name = "Invoice Number")
    sale_date       = models.DateField(default = timezone.now, verbose_name = "Sale Date")
    client_name     = models.ForeignKey(Client, on_delete = models.PROTECT, verbose_name = "Client Name")
    carting         = models.PositiveIntegerField(default = 0, verbose_name = "Carting")
    gstin           = models.CharField(blank = True, max_length = 15, verbose_name = "GSTIN")
    tax_type        = models.CharField(choices = CHOICES_TAX_TYPE, max_length = MAX_TAX_TYPE, verbose_name = "Tax Type")
    is_sample       = models.BooleanField(default = False, verbose_name = "Is this a Sample?")
    total_amount    = models.PositiveIntegerField(verbose_name = "Total Amount")
    amount_paid     = models.PositiveIntegerField(default=0, verbose_name = "Amount Paid")
    first_date      = models.DateField(default = timezone.now, verbose_name = "First Date of Payment")
    last_date       = models.DateField(default = timezone.now, verbose_name = "Last Date of Payment")
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name = "Created By")
    remarks         = models.CharField(blank= True, max_length=10, verbose_name = "Remarks")

    def __str__(self):
        return str(self.invoice_number)

# not to be displayed to anyone
class Bill(models.Model):

    invoice_number  = models.ForeignKey(Sale, on_delete = models.PROTECT, verbose_name = "Incoice Number")
    product_name    = models.ForeignKey(Product, on_delete = models.PROTECT, verbose_name = "Product Name")
    basic_rate      = models.PositiveIntegerField(blank = True, null = True, verbose_name = "Basic Cost")
    quantity        = models.PositiveIntegerField(verbose_name = "Quantity Supplied")
    igst            = models.DecimalField(decimal_places = 2, max_digits = 20, verbose_name = "IGST")
    cgst            = models.DecimalField(decimal_places = 2, max_digits = 20, verbose_name = "CGST")
    sgst            = models.DecimalField(decimal_places = 2, max_digits = 20, verbose_name = "SGST")
    export_sale     = models.DecimalField(decimal_places = 2, max_digits = 20, verbose_name = "Export Sale")
    # we do not need a created by here can fetch from Sales table
    # created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quantity)

class Payment(models.Model):
    invoice_number  = models.ForeignKey(Sale, on_delete = models.PROTECT, verbose_name = "Invoice Number")
    date            = models.DateField(default = timezone.now, verbose_name = "Date")
    amount_received = models.PositiveIntegerField(verbose_name = "Amount Received")
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name = "Created By")

    def __str__(self):
        return str (self.payment_received)

"""
    def publish(self):
        self.published_date = timezone.now()
        self.save()
"""
