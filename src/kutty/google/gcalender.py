# Google Calendar APIfrom __future__ import print_function
import os.path
import datetime as dt
import datetime
from typing import Dict, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from constants import SCOPES, READ_ONLY_SCOPES
from typing import Any, List, Optional, Union
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from googleapiclient.discovery import build

SCOPES = SCOPES
READ_ONLY_SCOPES = READ_ONLY_SCOPES

class GCalender:
    
    def __init__(self) -> None:
        """Initializes the GCalender class"""
        self.service = None
        self.creds = None
        self.calendar_id = "primary"
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
        """Gets the service for the user"""
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
            return "Service obtained"
        except Exception as e:
            print(e)
            return "Error occured"
    
    def display_events(self, max_results : int = 10):
        try:
            self.get_service()
            now = dt.datetime.utcnow().isoformat() + 'Z'
            event_result = self.service.events().list(calendarId=self.calendar_id, timeMin=now,
                                                       maxResults=10, singleEvents=True,
                                                       orderBy='startTime').execute()
            events = event_result.get('items', [])
            if not events:
                return "No upcoming events found."
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
        except Exception as e:
            print(e)
            return "Error occured"
        
    def create_event(self, event : Dict):
        """sample event={
            'summary': 'Google I/O 2023',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2023-08-18T09:00:00+05:00',
                'timeZone': 'IST',
                },
            'end': {
                'dateTime': '2023-08-18T17:00:00+05:00',
                'timeZone': 'IST',
                },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
                ],
            'attendees': [
                {'email': 'prakaasharun50@gmail.com'}
            ]
        }
    """
        try:
            self.get_service()
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            return "Event created"
        except HttpError as e:
            print(e)
            return "Error occured"
        
            
    def delete_event(self, event_id : str):
        """Deletes the event with the given event_id"""
        try:
            self.get_service()
            self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
            return "Event deleted"
        except HttpError as e:
            print(e)
            return "Error occured"
        





class GoogleCalendarReader(BaseReader):
    """Google Calendar reader.

    Reads events from Google Calendar

    """

    def load_data(
        self,
        number_of_results: Optional[int] = 100,
        start_date: Optional[Union[str, datetime.date]] = None,
    ) -> List[Document]:

    

        

        credentials = self._get_credentials()
        service = build("calendar", "v3", credentials=credentials)

        if start_date is None:
            start_date = datetime.date.today()
        elif isinstance(start_date, str):
            start_date = datetime.date.fromisoformat(start_date)

        start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
        start_datetime_utc = start_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_datetime_utc,
                maxResults=number_of_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            return []

        results = []
        for event in events:
            if "dateTime" in event["start"]:
                start_time = event["start"]["dateTime"]
            else:
                start_time = event["start"]["date"]

            if "dateTime" in event["end"]:
                end_time = event["end"]["dateTime"]
            else:
                end_time = event["end"]["date"]

            event_string = f"Status: {event['status']}, "
            event_string += f"Summary: {event['summary']}, "
            event_string += f"Start time: {start_time}, "
            event_string += f"End time: {end_time}, "

            organizer = event.get("organizer", {})
            display_name = organizer.get("displayName", "N/A")
            email = organizer.get("email", "N/A")
            if display_name != "N/A":
                event_string += f"Organizer: {display_name} ({email})"
            else:
                event_string += f"Organizer: {email}"

            results.append(Document(event_string))

        return results

    def _get_credentials(self) -> Any:
        """Gets the credentials for the user"""
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=3030)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds