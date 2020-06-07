# crm

**NOTE** : 
1. If you don't know anything about Django, go to https://tutorial.djangogirls.org/en/ , complete the tutorial and then start.
2. Got any error, what so ever. Follow simple steps :
   Just copy the error code -> Google It -> Click the first result (probably https://stackoverflow.com/ url)

### Pre-requisites
* git
* python>=3.5
* pip
* Reference for installation help https://tutorial.djangogirls.org/en/installation/

### Installation

In cmd,

1. **git clone https://github.com/ps-project/crm.git** (provide github username and password, when asked)
2. move in cmd to the folder and do **pip install -r requirements.txt** in cmd.
 (it will install django)

4. run **python manage.py makemigrations**
5. run **python manage.py migrate**
6. run **python manage.py createsuperuser**, set username and password.
7. run **python manage.py runserver**
  (it will start the website at http://127.0.0.1:8000/)
  
 login using the created username and password.
 
 **NOTE** : You have to perform step 4 and step 5 everytime you make changes to models.py
