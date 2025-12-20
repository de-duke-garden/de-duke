from main.settings.dev import *
import boto3
import os

import json

# Retrieve secret key from AWS Secrets Manager
try:
    SECRET_KEY_ARN = os.environ.get("SECRET_KEY_ARN")
    if SECRET_KEY_ARN:
        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION"))
        response = client.get_secret_value(SecretId=SECRET_KEY_ARN)
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        SECRET_KEY = secret_dict.get("secretkey")
except Exception as e:
    print(f"Error retrieving SECRET_KEY: {e}")

# Retrieve database credentials from AWS Secrets Manager
try:
    DATABASE_CREDENTIALS_ARN = os.environ.get("DATABASE_CREDENTIALS_ARN")
    if DATABASE_CREDENTIALS_ARN:
        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION"))
        response = client.get_secret_value(SecretId=DATABASE_CREDENTIALS_ARN)
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        DATABASES = {
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': secret_dict.get("dbname"),
                'USER': secret_dict.get("username"),
                'PASSWORD': secret_dict.get("password"),
                'HOST': secret_dict.get("host"),
                'PORT': secret_dict.get("port"),
            }
        }
except Exception as e:
    print(f"Error retrieving database credentials: {e}")

# Retrieve email credentials from AWS Secrets Manager
try:
    EMAIL_SECRET_ARN = os.environ.get("EMAIL_SECRET_ARN")
    if EMAIL_SECRET_ARN:
        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION"))
        response = client.get_secret_value(SecretId=EMAIL_SECRET_ARN)
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        EMAIL_HOST = secret_dict.get("host")
        EMAIL_PORT = secret_dict.get("port")
        EMAIL_HOST_USER = secret_dict.get("username")
        EMAIL_HOST_PASSWORD = secret_dict.get("password")
        EMAIL_USE_TLS = secret_dict.get("tls")
except Exception as e:
    print(f"Error retrieving email host password: {e}")


# Retrieve Google Map credentials from AWS Secrets Manager
try:
    GOOGLE_MAP_SECRET_ARN = os.environ.get("GOOGLE_MAP_SECRET_ARN")
    if GOOGLE_MAP_SECRET_ARN:
        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION"))
        response = client.get_secret_value(SecretId=GOOGLE_MAP_SECRET_ARN)
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        GOOGLE_MAP_API_KEY = secret_dict.get("apikey")
        MAP_WIDGETS["GoogleMap"]["apiKey"] = GOOGLE_MAP_API_KEY
except Exception as e:
    print(f"Error retrieving map API key: {e}")


DEBUG = True

# ALLOWED_HOSTS = ["de-duke.com", "www.de-duke.com"]
# ALLOWED_HOSTS = ["de-duke.com", "www.de-duke.com", ".compute.amazonaws.com"]

# CORS settings
# CORS_ALLOWED_ORIGINS = [
#     "https://de-duke.com",
#     "https://www.de-duke.com",
# ]
CORS_ALLOWED_ORIGINS = [
    "http://de-duke.com",
    "https://de-duke.com",
    "http://www.de-duke.com",
    "https://www.de-duke.com",
    "http://ec2-13-42-130-253.eu-west-2.compute.amazonaws.com",
]

# Trusted origins for CSRF and WebSocket origin checks
CSRF_TRUSTED_ORIGINS = [
    "https://de-duke.com",
    "https://www.de-duke.com",
    "https://ec2-13-42-130-253.eu-west-2.compute.amazonaws.com",
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
