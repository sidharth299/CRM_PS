#from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

#from .dbconf import *
from .constants import *

class Product(models.Model): 
    product_name = models.CharField(max_length = MAX_PRODUCT_NAME, unique = True)
    product_category = models.CharField(max_length = MAX_PRODUCT_CATEGORY,
                                        choices = CHOICES_PRODUCT_CATEGORY)
    hsn_code = models.PositiveIntegerField(blank = True, null=True)
    basic_rate = models.DecimalField(max_digits = 10,
                                    decimal_places = 2)
    tax_rate = models.DecimalField(max_digits = 4,
                                    decimal_places = 2)
    export_tax_rate = models.DecimalField(max_digits = 4, 
                                            decimal_places = 2)
    remarks = models.CharField(max_length = MAX_REMARKS, 
                                blank = True)

    def __str__(self):
        return self.product_name

class Client(models.Model):

    client_name = models.CharField(max_length = MAX_CLIENT_NAME, unique = True)
    gstin = models.CharField(max_length = 15, blank = True)
    client_category = models.CharField(max_length = MAX_CLIENT_CATEGORY, choices = CHOICES_CLIENT_CATEGORY)
    btc = models.CharField(blank = True, max_length = MAX_BTC, choices = CHOICES_BTC)
    telephone_main =  models.CharField(blank = True, max_length = 15)
    telephone_extra = models.CharField(blank = True, max_length = 15)
    email = models.EmailField(blank = True)
    contact_person = models.CharField(blank = True, max_length = MAX_CONTACT_PERSON)
    address = models.CharField(blank = True, max_length = MAX_ADDRESS)
    city = models.CharField(blank = True, max_length = MAX_CITY)
    pin_code = models.PositiveIntegerField(blank = True,null=True,validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    state = models.CharField(blank = True, max_length = MAX_STATE, default = DEFAULT_STATE, choices = CHOICES_STATE )
    country = models.CharField(blank  = True, max_length = MAX_COUNTRY, default = DEFAULT_COUNTRY, choices = CHOICES_COUNTRY)

    client_rank = models.PositiveSmallIntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(7)])
    lead_source = models.CharField(max_length = MAX_LEAD_SOURCE, choices = CHOICES_LEAD_SOURCE)
    remarks = models.CharField(blank = True, max_length = MAX_REMARKS)

    balance = models.DecimalField(default = 0, max_digits = 20, decimal_places = 2)
    latest_dsr_id = models.PositiveIntegerField(blank = True, null = True)

    def __str__(self):
        return self.client_name

    
    """
    main_product = models.ForeignKey(Product, on_delete = models.PROTECT)
    tax_type = models.CharField(max_length=3)
    tax = models.IntegerField(default=calculate(tax_type))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, default=1)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.product_name
    """