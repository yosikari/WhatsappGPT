from flask import Flask, request, jsonify

from services.openAI_api import chat_completion
from services.twilio_api import send_message

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
    try:
        # Extract incoming parameters from Twilio
        message = request.form['Body']
        sender_id = request.form['From']

        # Get response from OpenAI
        result = chat_completion(message)
        if result['status'] == 1:
            send_message(sender_id, result['response'])
    except:
        pass
    return 'OK', 200