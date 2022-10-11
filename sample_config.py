from os import urandom, path, environ
from datetime import timedelta
from functools import partial

from match.selection import serial_dictatorship, top_trading_cycle
from match.notification import email


# Web Server
CSRF_ENABLED = True
SECRET_KEY = urandom(30)
PROPAGATE_EXCEPTIONS = True
REMEMBER_COOKIE_NAME = 'match_token'            # Must be unique server-wide

# SQLAlchemy
basedir = path.abspath(path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(path.join(basedir, 'app.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Authentication
AUTH_METHOD = 'LDAP'
AUTH_URI = None
LDAP_URI = 'ldap://YOUR.LDAP.URI'
LDAP_SEARCH_BASE = 'ou=????,dc=????,dc=????'

# Admin
ADMIN_USERS = ['USER.ID.HERE']

# Match
ALLOCATION = top_trading_cycle

# Display
INFO_TEXT = (
    'Drag any number of options from the column on the left into your ranking '
    'on the right and sort in order of preference. Here is a link to '
    '<a href="LINK_HERE">more information</a>.'
)

# Email
EMAIL_HOST = 'smtp.gmail.com:587'
EMAIL_USER = 'YOUR.EMAIL@gmail.com'
EMAIL_PASSWORD = 'YOUR_APPLICATION_SPECIFIC_PASSWORD'
EMAIL_ADDENDUM = 'Any additional information you want in the message.'

# Notification
NOTIFICATION = partial(
    email, host=EMAIL_HOST, user=EMAIL_USER, password=EMAIL_PASSWORD,
    addendum=EMAIL_ADDENDUM
)
