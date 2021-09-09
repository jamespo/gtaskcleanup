gtaskcleanup.py
---------------

Remove completed tasks from google tasks


First Run
---------

Install requirements (Python 3 required)

	pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

- Go to Tasks API in Google Cloud Console and enable it
- Create Credentials (OAuth 2.0 Client ID)
- Download credentials
- Rename downloaded file to ~/.config/gtc-creds.json
- Run python script, browser will be lauched & you will be asked to authorize
- ~/.config/gtc-token.json should now be created


Usage
-----

	gtaskcleanup.py [list|delete]
