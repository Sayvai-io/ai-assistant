# Google Calendar APIfrom __future__ import print_function
import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from constants import SCOPES, READ_ONLY_SCOPES

SCOPES = SCOPES
READ_ONLY_SCOPES = READ_ONLY_SCOPES

class GCalender:
    
    def __init__(self) -> None:
        """Initializes the GCalender class"""
        self.service = None
        self.creds = None
        self.calendar_id = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        elif not self.creds or not self.creds.valid:
            self.creds = self.get_credentials()
            
        
    def get_credentials(self):
        """Gets the credentials for the user"""
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        self.creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(self.creds.to_json())
            
        return "Credentials obtained"
    
    def get_service(self):
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
            now = dt.datetime.utcnow().isoformat() + 'Z'
            event_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                       maxResults=10, singleEvents=True,
                                                       orderBy='startTime').execute()
            events = event_result.get('items', [])
            if not events:
                return "No upcoming events found."
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
            return "Done"
        except Exception as e:
            print(e)
            return "Error occured"


if __name__ == '__main__':
    gcalender = GCalender()
    # print(gcalender.get_service())
    