from flask import Flask, request, jsonify

from api.openAI_api import chat_complition, voice_trascript
from api.twilio_api import send_message
from api.openweather_api import get_weather
from services.user_service import add_user, get_user

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify(
        {
            'status': 'OK',
            'wehook_url': 'BASEURL/twilio/receiveMessage',
            'message': 'The webhook is ready.',
            'video_url': ''
        }
    )


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    # Extract incoming text-msg from Twilio
    message = request.form['Body']
    sender_id = request.form['From']

    # If it's new user add him to data
    if get_user(sender_id) == None:
        add_user(sender_id)
        send_message(sender_id, "*Welcome to SmartBox!*\n\nNow you can use ChatGPT, Dall-E-2, Midjourney, Weather API, Save notes, and more awesome fetchers!\n\n*Note:*\nFree trail users charges with\n ChatGPT: 30 messages,\n Dall-E-2: 3 generates,\n Midjourney: 3 generates.\n\n For more info, use \"/h\", \"/u\".")
        return 'OK', 200
    else:
        try:
            # Extract incoming voice-msg from Twilio
            voice = request.form['MediaUrl0']
            # Get transcript response from OpenAI
            res = voice_trascript(voice)
            prompt = str(res)
            send_message(sender_id, ('*Transcript:* \n \n' +
                                     prompt))
            # Get response from OpenAI / custom commends
            result = chat_complition(prompt, sender_id)
            send_message(sender_id, ('*GPT answer:* \n \n'
                                     + result['response']))
            return 'OK', 200
        except:
            pass

        try:
            if message[0:2] == '/w':
                if len(message) == 2:
                    weather = get_weather()
                    send_message(sender_id, weather)
                else:
                    weather = get_weather(message[3:len(message)])
                    send_message(sender_id, weather)
            else:
                # Get response from OpenAI / custom commends
                result = chat_complition(message, sender_id)
                send_message(sender_id, result['response'])
        except Exception as e:
            print('Text err:', e)
            pass
        return 'OK', 200
