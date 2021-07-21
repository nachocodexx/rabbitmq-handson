import calendar
import time
import json


class Message(object):
    def __init__(self, *args, **kwargs):
        self.value = kwargs.get('value', "HOLA")
        self.user_id = kwargs.get('user_id', "user_00")
        self.timestamp = calendar.timegm(time.gmtime())

    def toJSON(self):
        return json.dumps(self.__dict__)
