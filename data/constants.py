from django.contrib.sessions.backends.db import SessionStore
user_session = SessionStore()

## max values for NEW last two models ##

MAX_PERIOD = 10
MAX_ENTRY_TYPE = 18

CHOICES_ENTRY_TYPE = (
	("dealer_appointment","Dealer Appointment"),
	("a_letter","Appreciation Letter"),
	("converted","Converted"),
	("repeat","Repeat"),
	("big","Big Ticket Customer"),
)

###    defutl values   #####  

DEFAULT_STATE = 'Maharashtra'
DEFAULT_COUNTRY = 'India'
DEFAULT_ZONE="NAGPUR"
DEFAULT_LEAD_SOURCE="Others"

###    max values      #####

MAX_PRODUCT_NAME = 50
MAX_CLIENT_NAME = 50
MAX_CONTACT_PERSON = 50
MAX_CITY = 30


MAX_ADDRESS = 400
MAX_REMARKS = 2000

MAX_INVOICE_NUMBER = 15
## all category max_legths

MAX_PRODUCT_CATEGORY = 30
MAX_CLIENT_CATEGORY = 15
MAX_BTC = 8
MAX_LEAD_SOURCE = 10
MAX_COUNTRY = 8
MAX_STATE = 30

MAX_CONTACT_MODE = 12
MAX_TAX_TYPE = 20
MAX_SAMPLE_STATUS = 8

MAX_ZONE=8


####   choices     ###
## IMPORTANT !!! updated the max_legth above also when you make add any new element to the categories


CHOICES_SAMPLE_STATUS = (
	("Sent","Sent"),
	("Pending","Pending"),
	("Passed","Passed"),
	("Failed","Failed"),
)

CHOICES_TAX_TYPE = (
	("Maharashtra","Maharashtra"),
	("Outside Maharashtra","Outside Maharashtra"),
	("Indirect Export","Indirect Export"),
	("Direct Export","Direct Export"),
)

CHOICES_CONTACT_MODE = (
	("Visit","Visit"),
	("Telephone","Telephone"),
	("Email","Email"),
	("WhatsApp","WhatsApp"),
	("No Response","No Response"),
	("Others", "Others"),
)


CHOICES_PRODUCT_CATEGORY = ( 
    ("Agro Chemical","Agro Chemical"), 
    ("Defoamer Chemical", "Defoamer Chemical"), 
    ("Textile Industry Chemical", "Textile Industry Chemical"), 
    ("Cosmetics Industry Chemical", "Cosmetics Industry Chemical"), 
    ("Construction Chemical", "Construction Chemical"), 
    ("Mining Insutry Chemical", "Mining Insutry Chemical"), 
    ("Paper Insutry Chemical", "Paper Insutry Chemical"), 
    ("Others", "Others"), 
)

CHOICES_CLIENT_CATEGORY = ( 
    ("Agrochem","Agrochem"), 
    ("Construction","Construction"), 
    ("Others","Others"), 
)

CHOICES_BTC = ( 
    ("Non BTC","Non BTC"), 
    ("BTC-1", "BTC-1"), 
    ("BTC-2", "BTC-2"), 
)

CHOICES_LEAD_SOURCE = ( 
    ("Reference","Reference"), 
    ("Indiamart", "Indiamart"), 
    ("Others", "Others"), 
)

CHOICES_COUNTRY = (
	("India","India"),
	("Overseas","Overseas"),
	)

CHOICES_ZONE=(
	("NORTH","NORTH"),
	("SOUTH","SOUTH"),
	("EAST","EAST"),
	("WEST","WEST"),
	("CENTRAL","CENTRAL"),
	("EXPORT","EXPORT"),
	("NAGPUR","NAGPUR"),
)

CHOICES_STATE = (
	("Andhra Pradesh","Andhra Pradesh"),
	("Arunachal Pradesh ","Arunachal Pradesh "),
	("Assam","Assam"),
	("Bihar","Bihar"),
	("Chhattisgarh","Chhattisgarh"),
	("Goa","Goa"),
	("Gujarat","Gujarat"),
	("Haryana","Haryana"),
	("Himachal Pradesh","Himachal Pradesh"),
	("Jharkhand","Jharkhand"),
	("Karnataka","Karnataka"),
	("Kerala","Kerala"),
	("Madhya Pradesh","Madhya Pradesh"),
	("Maharashtra","Maharashtra"),
	("Manipur","Manipur"),
	("Meghalaya", "Meghalaya"),
	("Mizoram","Mizoram"),
	("Nagaland","Nagaland"),
	("Odisha","Odisha"),
	("Punjab","Punjab"),
	("Rajasthan","Rajasthan"),
	("Sikkim","Sikkim"),
	("Tamil Nadu","Tamil Nadu"),
	("Telangana","Telangana"),
	("Tripura","Tripura"),
	("Uttar Pradesh","Uttar Pradesh"),
	("Uttarakhand","Uttarakhand"),
	("West Bengal","West Bengal"),
	("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
	("Chandigarh","Chandigarh"),
	("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
	("Daman and Diu","Daman and Diu"),
	("Delhi","Delhi"),
	("Jammu and Kashmir","Jammu and Kashmir"),
	("Ladakh","Ladakh"),
	("Lakshadweep","Lakshadweep"),
	("Puducherry","Puducherry"),
)