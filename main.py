import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import discord
from discord.ext import commands

SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
      "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)
calendarId = 'not for dog'

@bot.event
async def on_scheduled_event_create(event):
    start_time = event.start_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    end_time = event.end_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')

    event = {
        'summary': event.name,
        'location': event.location,
        'description': event.description,
        'start': {
            'dateTime': start_time,
        },
        'end': {
            'dateTime': end_time,
        },
        'id': event.id,

        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }
    event = service.events().insert(calendarId=calendarId, body=event).execute()

@bot.event
async def on_scheduled_event_delete(event):
    event = service.events().delete(calendarId=calendarId, eventId = event.id).execute()

@bot.event
async def on_scheduled_event_update(before, after):
    event = service.events().get(calendarId = calendarId, eventId = after.id).execute()
    end_time = after.end_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    start_time = after.start_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')

    event['summary'] = after.name
    event['location'] = after.location
    event['description'] = after.description
    event['start']['dateTime'] = start_time
    event['end']['dateTime'] = end_time

    event = service.events().update(calendarId=calendarId, eventId=after.id, body=event).execute()



bot.run('not for dog')
