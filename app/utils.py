import random
from twilio.rest import Client


def send_sms(body, number):
    account_id = "your account_id"
    auth_token = "your auth_token"
    client = Client(account_id, auth_token)
    messages = client.messages.create(
        body=body,
        from_='+13613093414',
        to=number
    )


def generate_verification_code():
    return str(random.randint(100000, 999999))