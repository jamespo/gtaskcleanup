#!/bin/env python3

# gtaskcleanup.py

import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pprint import pprint


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']


def getcreds():
    """get the credentials"""
    credfile = os.path.expanduser("~/.config/gtc-creds.json")
    tokenfile = os.path.expanduser("~/.config/gtc-token.json")
    creds = None
    # tokenfile stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenfile):
        creds = Credentials.from_authorized_user_file(tokenfile, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credfile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenfile, 'w') as token:
            token.write(creds.to_json())
    return creds


def listtasks(service):
    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])

    if not items:
        print('No task lists found.')
    else:
        print('Task lists:')
        for item in items:
            print(u'{0} ({1})'.format(item['title'], item['id']))
            taskresults = service.tasks().list(tasklist=item['id'],
                                               showCompleted=True,
                                               showHidden=True).execute()
            # tasks = taskresults.get()
            # for task in tasks["items"]:
            #     print("%s", task["title"])
            if taskresults.get('items'):
                pprint(taskresults['items'])


def main():
    """either lists or deletes completed/hidden tasks
    """
    action = 'list'
    try:
        action = sys.argv[1]
    except:
        pass
    creds = getcreds()
    service = build('tasks', 'v1', credentials=creds)

    if action == "list":
        listtasks(service)


if __name__ == '__main__':
    main()
