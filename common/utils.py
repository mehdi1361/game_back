from system.models import SmsSender
from kavenegar import *
from django.conf import settings


class Kavenegar:
    def __init__(self, receptor=None, message=None):
        self.message = message
        self.receptor = receptor
        self.api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        self.sender = settings.KAVENEGAR_SENDER

    def run(self):
        if self.receptor is None:
            return False

        params = {
            'sender': self.sender,
            'receptor': self.receptor,
            'message': self.message
        }
        response = self.api.sms_send(params)

        if response[0]['status'] == 1:
            return True

        return False


class Inline:
    def __init__(self, mobile_nu, message):
        self.mobile = mobile_nu
        self.message = message

    def run(self):
        url = "http://sitenevis.com/gameport.php"
        querystring = {"phone": self.mobile, "body": self.message}

        headers = {
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.text == '1':
            return True

        return False
