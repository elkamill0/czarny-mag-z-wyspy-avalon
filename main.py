import datetime
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import discord
from discord.ext import commands, tasks
import check_plans


with open('json/ids.json') as f:
    json_data = json.load(f)
    calendarId = json_data['calendarId']
    bot_token = json_data['discord_bot_token']
    discord_bot_channel_id = json_data['discord_bot_channel_id']



SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds = None
if os.path.exists("json/token.json"):
    creds = Credentials.from_authorized_user_file("json/token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
      "json/credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    with open("json/token.json", "w") as token:
        token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print("Done!")
    send_msg.start()


@bot.command()
async def poll(ctx, *s):
    emotes = ['🟢', '🔴', '🟡', '🔵', '🟠', '🟣', '⚪', '⚫']

    s = " ".join(s)
    s = s.split(":")
    q = s[0]
    a = s[1].split(",")

    mess = "# **" + q + "**" + '\n'
    for i, e in zip(a, emotes):
        mess += e + " " + i + '\n'
    message = await ctx.send(mess)
    for e in range(len(a)):
        await message.add_reaction(emotes[e])

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
async def on_scheduled_event_update(after):
    event = service.events().get(calendarId = calendarId, eventId = after.id).execute()
    end_time = after.end_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    start_time = after.start_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')

    event['summary'] = after.name
    event['location'] = after.location
    event['description'] = after.description
    event['start']['dateTime'] = start_time
    event['end']['dateTime'] = end_time

    event = service.events().update(calendarId=calendarId, eventId=after.id, body=event).execute()

@tasks.loop(minutes=30.0)
async def send_msg():
    messages = check_plans.check()
    channel = bot.get_channel(discord_bot_channel_id)
    print(messages)
    if messages:
        for mess in messages:
            await channel.send(mess)

bot.run(bot_token)