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

from load_json import Load_jsons
from facebook_integration import Fb
from google_calendar_integration import Calendar
from polls import polling2

json_ids = Load_jsons()
calendar = Calendar()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print("Done!")
    # send_msg.start()


@bot.command()
async def poll(ctx, *s):
    message, reactions = polling2(s)
    message = await ctx.send(message)
    for r in reactions:
        await message.add_reaction(r)

@bot.event
async def on_scheduled_event_create(event):
    calendar.create_event(event)

@bot.event
async def on_scheduled_event_delete(event):
    calendar.delete_event(event)

@bot.event
async def on_scheduled_event_update(before, after):
    calendar.update_event(after)

@tasks.loop(minutes=30)
async def send_msg():
    messages = check_plans.check()
    channel = bot.get_channel(json_ids.discord_channels_planChannelId())
    if messages and channel:
        await channel.send(f'New {len(messages)} changes found!')
        for mess in messages:
            message =mess.split('+')
            await channel.send(f'{message[2]}: [{message[1]}]({message[0]})')

@bot.command()
async def post_schedule(ctx):
    fb = Fb()
    if ctx.message.channel.id != json_ids.discord_channels_mediaChannelId():
        return 0
    guild = bot.guilds[0]
    start_time, end_time = fb.time()
    await guild.create_scheduled_event(name=fb.name(), start_time=start_time, location="Aula C1", end_time=end_time, description=fb.description(), entity_type=discord.EntityType.external, privacy_level=discord.PrivacyLevel.guild_only)

bot.run(json_ids.discord_bot_token())