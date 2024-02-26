import json

class Load_jsons:
    def __init__(self):
        self.f = open("json/ids.json", "r")
        self.data = json.load(self.f)
        self.f.close()
    def discord_bot_token(self):
        return self.data['discord']['bot']['token']
    def discord_channels_planChannelId(self):
        return self.data['discord']['channels']['planChannelId']
    def discord_channels_mediaChannelId(self):
        return self.data['discord']['channels']['mediaChannelId']
    def calendar_calendarId(self):
        return self.data['calendar']['calendarId']
    def facebook_appId(self):
        return self.data['facebook']['appId']
    def facebook_accessToken(self):
        return self.data['facebook']['accessToken']
    def facebook_objectId(self):
        return self.data['facebook']['objectId']
