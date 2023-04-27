import os

from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')
client = Client(account_sid, auth_token)


def send_message(to, message) -> None:
    '''
    Send message to a Telegram user.
    Parameters:
        - to(str): sender whatsapp number in this whatsapp:+919558515995 form
        - message(str): text message to send
    Returns:
        - None
    '''
    try:
        if message[0:10] == 'https://ap':
            _ = client.messages.create(
                from_='whatsapp:+14155238886',
                body='Midjourney  Generate.',
                media_url=message,
                to=to
            )
            print('\n Output: Midjourny url:', message, '\n\n')
            return 'OK', 200
        elif message[0:4] == 'http':
            _ = client.messages.create(
                from_='whatsapp:+14155238886',
                body='Dall-E-2 Generate.',
                media_url=message,
                to=to
            )
            print('\n Output: Dall-E-2 url:', message, '\n\n')
            return 'OK', 200

        else:
            _ = client.messages.create(
                from_='whatsapp:+14155238886',
                body=message,
                to=to
            )
            print('\n Output: ', message, '\n\n')
            return 'OK', 200
    except Exception as e:
        print('Twilio Error: ', e)


def send_voice_message(to, mp3_file):
    client = Client(account_sid, auth_token)

    _ = client.messages.create(
        from_='whatsapp:+14155238886',
        body='',
        to=to,
        media_url=mp3_file,
    )

    return 'OK', 200
