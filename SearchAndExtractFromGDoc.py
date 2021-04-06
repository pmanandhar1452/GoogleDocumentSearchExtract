__author__ = "Prakash Manandhar"
__copyright__ = "Copyright 2021, Prakash Manandhar"
__credits__ = ["Prakash Manandhar"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prakash Manandhar"
__email__ = "prakashm@alum.mit.edu"
__status__ = "Production"

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import argparse

def init_argparse():
    parser = argparse.ArgumentParser(description='Search and extract from google docs document.')
    parser.add_argument('--id', help='Google Document GUID', required=True)
    parser.add_argument('--token', help='Token File', required=True)
    parser.add_argument('--secret', help='Client Secret File', required=True)
    parser.add_argument('--regex', help='Regular Expression', required=True)
    parser.add_argument('--outfile', help='Output File', required=True)
    return parser

if __name__ == "__main__":
    parser = init_argparse()
    args, unknwon_args = parser.parse_known_args()
    
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(args.token):
        creds = Credentials.from_authorized_user_file(args.token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                args.secret, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(args.token, 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    print("Retrieving document ....")
    document = service.documents().get(documentId=args.id).execute()

    print('The title of the document is: {}'.format(document.get('title')))

    