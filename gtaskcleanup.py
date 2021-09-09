#!/bin/env python3

# gtaskcleanup.py
# USAGE: gtaskcleanup.py [list|delete]

import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def getcreds():
    """get the credentials"""
    credfile = os.path.expanduser("~/.config/gtc-creds.json")
    tokenfile = os.path.expanduser("~/.config/gtc-token.json")
    creds = None
    # tokenfile stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenfile):
        scopes = ['https://www.googleapis.com/auth/tasks']
        creds = Credentials.from_authorized_user_file(tokenfile, scopes)
    # no creds - user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credfile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save newly issued token
        with open(tokenfile, 'w') as token:
            token.write(creds.to_json())
    return creds


def taskaction(service, delete=False):
    """list the tasks & optionally delete"""
    maxitems = 150
    results = service.tasklists().list(maxResults=maxitems).execute()
    tasklists = results.get('items', [])

    if not tasklists:
        print('No task lists found.')
    else:
        if delete:
            print("*** Deleting ***\n")
        for tasklist in tasklists:
            print('%s' % tasklist['title'])
            taskresults = service.tasks().list(tasklist=tasklist['id'],
                                               maxResults=maxitems,
                                               showCompleted=True,
                                               showHidden=True).execute()
            if taskresults.get('items'):
                for task in taskresults['items']:
                    if task['status'] == 'completed':
                        print('  * %s' % task['title'])
                        if delete:
                            service.tasks().delete(tasklist=tasklist['id'],
                                                   task=task['id']).execute()


def main():
    """either lists or deletes completed/hidden tasks"""
    action = 'list'
    try:
        action = sys.argv[1]
    except IndexError:
        pass
    creds = getcreds()
    service = build('tasks', 'v1', credentials=creds)

    if action == "list":
        taskaction(service)
    elif action == "delete":
        taskaction(service, delete=True)


if __name__ == '__main__':
    main()
