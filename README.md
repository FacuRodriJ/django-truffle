# Django and Truffle

## Requirements

- Python 3.6.5 or higher
- Pip 18.0 or higher
- Npm 6.4.1 or higher

## Installation

### Django

First create the virtual environment, run the following command in the root directory:

    python -m venv .venv

To activate the environment, run the following command:
    
    source .venv/bin/activate

To install the dependencies, run the following command:

    pip install -r requirements.txt


### Truffle

To install Truffle, run the following command:

    npm install -g truffle


## Running

To run the Django server, run the followings command:

    python manage.py makemigrations
    
    python manage.py migrate
    
    python manage.py createsuperuser

To install static dependencies, run the following command in the `django_setup/static` directory:

    npm install

To run the Django server, run the following command in the `django_setup/` directory:

    python manage.py runserver
    

