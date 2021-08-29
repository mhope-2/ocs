## REST API for an Online Clothing Store using Django REST Framework

### Getting Started

First clone the repository from Github and switch to the project directory:

    $ git clone https://github.com/mhope-2/ocs
    $ cd ocs
    
Create a Vitual Environment (Linux, Mac)

    $ python3 -m venv env

Activate the virtualenv for your project

    $ source env/bin/activate
    
Install project requirements:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver


### Further Improvements
```
-[x] Dockerize the application  
-[x] Allow admin to apply taxes and discounts

```