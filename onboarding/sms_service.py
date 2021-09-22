from twilio.rest import Client
from django.conf import settings


class SMSService:

    def send_sms(self, mobile_number, text_message, country_code=None, request_id=None):
        print("@@@@@____", mobile_number)
        account_sid = settings.TWILIO_ACCOUNT_ID
        auth_token = settings.TWILIO_AUTH_TOKEN

        client = Client(account_sid, auth_token)
        client.messages.create(to=mobile_number, from_=settings.TWILIO_NUMBER, body=text_message)
