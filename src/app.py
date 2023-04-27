from flask import Flask, request, jsonify

from api.openAI_api import chat_complition, voice_trascript
from api.twilio_api import send_message, send_voice_message
from api.openweather_api import get_weather
from api.play_ht_api import text_to_mp3
from api.google_api import text_to_wav
from services.user_service import add_user, get_user, update_user_counter
from services.data_api_service import count_words


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
# text_to_wav("en-AU-Neural2-A", "What is the temperature in Sydney?")


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    print('\n\n From:', request.form['From'])
    print(' Input:', request.form['Body'])
    # Extract incoming text-msg from Twilio
    message = request.form['Body']
    sender_id = request.form['From']

    # If it's new user add him to data
    if get_user(sender_id) == None:
        add_user(sender_id)
        send_message(sender_id, "*Welcome to SmartBox!*\n\nNow you can use ChatGPT, Dall-E-2, Midjourney, Weather API, Save notes, and more awesome fetchers!\n\n*Note:*\nFree trail users charges with\n ChatGPT: 30 messages,\n Dall-E-2: 3 generates,\n Midjourney: 3 generates.\n Text to speech: 30 words.\n\n For more info, use \"/h\", \"/u\".\n\nhttps://www.youtube.com/watch?v=JiPVyhliryw")
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
            if message.startswith('/v '):
                # define a dictionary that maps the language code
                VOICE_MAP = {'he': 'he-IL-Standard-B',
                             'he2': 'he-IL-Wavenet-C',
                             'ru': 'ru-RU-Wavenet-D',
                             'ru2': 'ru-RU-Wavenet-C',
                             'en': 'en-US-Standard-D'}

                # get language code from message
                lang = message[3:5]

                # get the corresponding voice name for the language code, default to English
                voice_name = VOICE_MAP.get(lang, '')

                # get the text from the message
                txt = message[5:] if voice_name else message[2:]

                # handle lang v2
                if message[3:6] == 'he2':
                    voice_name = 'he-IL-Wavenet-C'
                    txt = message[6:]
                if message[3:6] == 'ru2':
                    voice_name = 'ru-RU-Wavenet-C'
                    txt = message[6:]

                # get the word count
                count = count_words(txt)

                # get the current user
                currUser = get_user(sender_id)

                # check if the user has enough playht to convert the text to voice
                if int(currUser['playht']) >= count:
                    # update the playht counter
                    update_user_counter(sender_id, 'playht', str(
                        int(currUser['playht'])-count))

                    # convert text to voice and send it
                    voiceUrl = text_to_wav(
                        voice_name, txt) if voice_name else text_to_mp3(txt)
                    send_voice_message(sender_id, voiceUrl)
                else:
                    # send an error message if the user doesn't have enough playht
                    res = f"Sorry you have only {currUser['playht']} words to convert to voice."
                    send_message(sender_id, res)

            elif message.startswith('/w'):
                if len(message) == 2:
                    weather = get_weather()
                    send_message(sender_id, weather)
                else:
                    weather = get_weather(message[3:])
                    send_message(sender_id, weather)
            else:
                # Get response from OpenAI / custom commends
                result = chat_complition(message, sender_id)
                send_message(sender_id, result['response'])
        except Exception as e:
            print('Text err:', e)
            pass
        return 'OK', 200
