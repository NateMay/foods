
# Copy this file to github_settings.py (don't check it into github)

# Go to https://github.com/settings/developers

# Add a New OAuth2 App 

# Using ngrok is hard because the url changes every time you start ngrok

# If you are running on localhost, here are some settings:

# Application name: Review Local
# Homepage Url: http://localhost:8000
# Application Description: Whatever
# Authorization callback URL: http://127.0.0.1:8000/oauth/complete/github/


# Using PythonAnywhere here are some settings:

# Application name: Review PythonAnywhere
# Homepage Url: https://natmay.pythonanywhere.com
# Application Description: Whatever
# Authorization callback URL: https://natmay.pythonanywhere.com/oauth/complete/github/

# Also on PythonAnywhere, go into the Web tab and enable "Force HTTPS"
# so you don't get a redirect URI mismatch.

# Then copy the client_key and secret to this file

SOCIAL_AUTH_GITHUB_KEY = '33eae2fa3fe1b9df8c3e'
SOCIAL_AUTH_GITHUB_SECRET = '0ec91e5d0a8416bd3869cc12425f9a335f01dd7d'

# For detail: https://readthedocs.org/projects/python-social-auth/downloads/pdf/latest/
