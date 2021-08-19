from typing import List
import os

# Branding name
BRANDING_NAME = "TJ Schedules"

# DEBUG and authorized hosts
DEBUG = False
ALLOWED_HOSTS: List[str] = []

# secret
SECRET_KEY = "supersecret"

# OAuth
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_ION_KEY = "ionkeywowsocool"
SOCIAL_AUTH_ION_SECRET = "ionsecretwowsocool"

# Message blast - treated as HTML safe text
# type is str
GLOBAL_MESSAGE = "<b>WARNING</b>: This is not ready for production usage! Any and all data may be deleted at any time without warning!"
