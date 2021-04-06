__author__ = "Prakash Manandhar"
__copyright__ = "Copyright 2021, Prakash Manandhar"
__credits__ = ["Prakash Manandhar"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prakash Manandhar"
__email__ = "prakashm@alum.mit.edu"
__status__ = "Production"

import argparse
import re
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def init_argparse():
    parser = argparse.ArgumentParser(description='Search and extract from google docs document.')
    parser.add_argument('--id', help='Google Document GUID', required=True)
    parser.add_argument('--token', help='Token File', required=True)
    parser.add_argument('--secret', help='Client Secret File', required=True)
    parser.add_argument('--regex', help='Regular Expression', required=True)
    parser.add_argument('--outfile', help='Output File', required=True)
    return parser

"""
Source: https://developers.google.com/docs/api/samples/extract-text#python
"""
def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

"""
Source: https://developers.google.com/docs/api/samples/extract-text#python
"""
def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text

def find_text(doc_text, regex, outfile):
    with open(outfile, 'w') as fp:  
        fp.write("MatchID,MatchText\n")
        matches = re.findall(regex, doc_text)
        print(f"Found {len(matches)} matches ...")
        i = 1
        for m in matches:
            fp.write(f"{i},{m}\n")
            i = i + 1

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

    doc_content = document.get('body').get('content')
    doc_text = read_strucutural_elements(doc_content)

    find_text(doc_text, args.regex, args.outfile)

    