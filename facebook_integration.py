from pyfacebook import GraphAPI
import datetime
from load_json import Load_jsons

json_ids = Load_jsons()

class Fb:
    def __init__(self):
        self.api = GraphAPI(app_id=json_ids.facebook_appId(), access_token=json_ids.facebook_accessToken())
        self.data = self.api.get_object(object_id=json_ids.facebook_objectId())
    def name(self):
        return self.data['data'][0]['name']
    def time(self):
        start_time = self.data['data'][0]['start_time']
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
        deltatime = datetime.timedelta(minutes=90)
        end_time = start_time + deltatime
        return start_time, end_time
    def id(self):
        return self.data['data'][0]['id']
    def description(self):
        return "https://www.facebook.com/events/" + str(self.id())

