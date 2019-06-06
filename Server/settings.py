from datetime import timedelta
import os

# Flask settings
SECRET_KEY = 'dj8.a0dq5pjT1!2N3,E82dlv434ma843nv'
DEBUG = True
BOOTSTRAP_SERVE_LOCAL = True
PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)

# Database
DB_NAME = os.getenv('DB_NAME','netdiag')
DB_PORT = os.getenv('DB_PORT', 27017)
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_AUTHDB = os.getenv("DB_AUTHDB") # Def is admin
DB_AUTHMECH = os.getenv("DB_AUTHMECH") # Def is salted SHA1

# Site settings
SITE_URL = "NetDiag - Oh, so you want data to diagnose issues?"

# Email
EMAIL_SERVER = 'mxsb.tn.gov'
EMAIL_SERVER_PORT = '25'
EMAIL_USER = 'chris.babcock@tn.gov'
EMAIL_PASSWORD = ''