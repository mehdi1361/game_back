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
