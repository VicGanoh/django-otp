# Django OTP Verification
## Overview
This Django playground project implements OTP (One-Time Password) verification for user authentication using pyotp. OTP verification adds an extra layer of security by requiring users to enter a temporary code sent to their registered phone number in addition to their password.

## Features

- User model with phone number authentication
- Custom user manager for creating users and superusers
- OTPVerification model for managing OTP codes and verification status
- Automatic generation of secret keys and OTP codes
- Verification of OTP codes against the generated OTP
- Handling of OTP expiration and verification status

## Installation
Inside your terminal clone the repository:
```
git clone https://github.com/VicGanoh/django-otp.git
```

In your terminal navigate to the repository:
```
cd django-otp
```
Create a virtual env and activate it:
```
python -m venv [your preffered virtual environment name]
```

Activate the virtual env:
```
source [name of your virtual env]/bin/activate
```

Install dependencies using pip:
```
pip install -r requirements.txt
```
Apply database migration:
```
python manage.py makemigrations
python manage.py migrate
```

Create a superuser for accessing django admin:
```
python manage.py createsuperuser
```

Start the development server:
```
python manage.py runserver
```


## Usage


## Contributions
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

