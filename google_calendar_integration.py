from load_json import Load_jsons
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

json_ids = Load_jsons()


class Calendar:
    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]
        self.creds = None

        if os.path.exists("json/token.json"):
            self.creds = Credentials.from_authorized_user_file("json/token.json", self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "json/credentials.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open("json/token.json", "w") as token:
                token.write(self.creds.to_json())

        self.service = (build('calendar', 'v3', credentials=self.creds))

    def create_event(self, e):
        event = {
            'summary': e.name,
            'location': e.location,
            'description': e.description,
            'start': {
                'dateTime': e.start_time.strftime('%Y-%m-%dT%H:%M:%S+00:00'),
            },
            'end': {
                'dateTime': e.end_time.strftime('%Y-%m-%dT%H:%M:%S+00:00'),
            },
            'id': e.id
        }
        return self.service.events().insert(calendarId=json_ids.calendar_calendarId(), body=event).execute()

    def delete_event(self, e):
        return self.service.events().delete(calendarId=json_ids.calendar_calendarId(), eventId=e.id).execute()

    def update_event(self, after):
        event = self.service.events().get(calendarId=json_ids.calendar_calendarId(), eventId=after.id).execute()
        end_time = after.end_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        start_time = after.start_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')

        event['summary'] = after.name
        event['location'] = after.location
        event['description'] = after.description
        event['start']['dateTime'] = start_time
        event['end']['dateTime'] = end_time

        return self.service.events().update(calendarId=json_ids.calendar_calendarId(), eventId=after.id,
                                            body=event).execute()




