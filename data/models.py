from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

#from .dbconf import *
from .constants import *

# has to have add some of the null=True only for the time being will fix it when backend will be populating the data instead 

# add/changed by only admin
class Product(models.Model): 
    product_name     = models.CharField(max_length = MAX_PRODUCT_NAME, unique = True)
    product_category = models.CharField(choices = CHOICES_PRODUCT_CATEGORY, max_length = MAX_PRODUCT_CATEGORY)
    hsn_code         = models.PositiveIntegerField(null=True)
    basic_rate       = models.PositiveIntegerField()
    tax_rate         = models.DecimalField(decimal_places = 2, max_digits = 4)
    export_tax_rate  = models.DecimalField(decimal_places = 2, max_digits = 4)
    remarks          = models.CharField(blank = True, max_length = MAX_REMARKS)
    created_by       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class Client(models.Model):

    client_name      = models.CharField(max_length = MAX_CLIENT_NAME, unique = True)
    gstin            = models.CharField(blank = True, max_length = 15)
    client_category  = models.CharField(choices = CHOICES_CLIENT_CATEGORY, max_length = MAX_CLIENT_CATEGORY)
    btc              = models.CharField(blank = True, choices = CHOICES_BTC, max_length = MAX_BTC)
    telephone_main   = models.CharField(blank = True, max_length = 15)
    telephone_extra  = models.CharField(blank = True, max_length = 15)
    email            = models.EmailField(blank = True)
    contact_person   = models.CharField(blank = True, max_length = MAX_CONTACT_PERSON)
    address          = models.CharField(blank = True, max_length = MAX_ADDRESS)
    city             = models.CharField(blank = True, max_length = MAX_CITY)
    pin_code         = models.PositiveIntegerField(blank = True, null=True, validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    state            = models.CharField(blank = True, choices = CHOICES_STATE , default = DEFAULT_STATE, max_length = MAX_STATE)
    country          = models.CharField(blank  = True, choices = CHOICES_COUNTRY, default = DEFAULT_COUNTRY, max_length = MAX_COUNTRY)
    zone             = models.CharField(blank=True , choices=CHOICES_ZONE, default= DEFAULT_ZONE, max_length=MAX_ZONE)
    client_rank      = models.PositiveSmallIntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(7)])
    lead_source      = models.CharField(choices = CHOICES_LEAD_SOURCE, default=DEFAULT_LEAD_SOURCE, max_length = MAX_LEAD_SOURCE)
    remarks          = models.CharField(blank = True, max_length = MAX_REMARKS)
    balance          = models.IntegerField(default = 0)
    latest_dsr_id    = models.PositiveIntegerField(blank = True, null = True)
    created_by       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


    def __str__(self):
        return self.client_name

class Dsr(models.Model):

    client_id       = models.ForeignKey(Client, on_delete = models.PROTECT)
    contact_person  = models.CharField(blank = True, max_length = MAX_CONTACT_PERSON)
    telephone       = models.CharField(blank = True, max_length = 15)
    email           = models.EmailField(blank = True)
    contact_mode    = models.CharField(choices = CHOICES_CONTACT_MODE, max_length = MAX_CONTACT_MODE)
    date_of_contact = models.DateField(default = timezone.now)
    action          = models.CharField(max_length = MAX_REMARKS)
    product_id      = models.ForeignKey(Product, blank = True, null = True,on_delete = models.PROTECT)
    next_call_date  = models.DateField()
    sample_status   = models.CharField(blank = True, choices = CHOICES_SAMPLE_STATUS, max_length = MAX_SAMPLE_STATUS) 
    client_rank     = models.PositiveSmallIntegerField(default = 1, validators = [MinValueValidator(1), MaxValueValidator(7)])
    failed_sale     = models.BooleanField(default = False) 
    successful_sale = models.BooleanField(default = False)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.action

class Sample(models.Model):

    client_id       = models.ForeignKey(Client, on_delete = models.PROTECT)
    sent_date       = models.DateField(default = timezone.now)
    city            = models.CharField(blank = True, max_length = MAX_CITY)
    product_id      = models.ForeignKey(Product, blank = True, null = True, on_delete = models.PROTECT)
    sample_quantity = models.PositiveIntegerField()
    sample_status   = models.CharField(choices = CHOICES_SAMPLE_STATUS, max_length = MAX_SAMPLE_STATUS)
    remarks         = models.CharField(blank = True, max_length = MAX_REMARKS)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product_id)

# only Admin/Accountants
class Sale(models.Model):

    invoice_number  = models.AutoField(primary_key = True)
    sale_date       = models.DateField(default = timezone.now)
    client_id       = models.ForeignKey(Client, on_delete = models.PROTECT)
    carting         = models.PositiveIntegerField(default = 0 )
    gstin           = models.CharField(blank = True, max_length = 15)
    tax_type        = models.CharField(choices = CHOICES_TAX_TYPE, max_length = MAX_TAX_TYPE)
    is_sample       = models.BooleanField(default = False)
    total_amount    = models.PositiveIntegerField()
    amount_paid     = models.PositiveIntegerField()
    fisrt_date      = models.DateField(default = timezone.now)
    last_date       = models.DateField(default = timezone.now)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.invoice_number

# not to be displayed to anyone
class Bill(models.Model):
    
    invoice_number  = models.ForeignKey(Sale, on_delete = models.PROTECT)
    product_id      = models.ForeignKey(Product, on_delete = models.PROTECT)
    basic_rate      = models.PositiveIntegerField(blank = True, null = True)
    quantity        = models.PositiveIntegerField()
    igst            = models.DecimalField(decimal_places = 2, max_digits = 20)   
    cgst            = models.DecimalField(decimal_places = 2, max_digits = 20)  
    sgst            = models.DecimalField(decimal_places = 2, max_digits = 20)
    export_sale     = models.DecimalField(decimal_places = 2, max_digits = 20)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_id

class Payment(models.Model):
    invoice_number  = models.ForeignKey(Sale, on_delete = models.PROTECT)
    date            = models.DateField(default = timezone.now)
    amount_received = models.PositiveIntegerField()
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.payment_recieved

"""
    def publish(self):
        self.published_date = timezone.now()
        self.save()
"""