import os
import requests
import json
from dotenv import load_dotenv
import time
from services.data_api_service import update_api_counter, get_data_api
load_dotenv()


api_key = os.getenv('PLAY_HT_KEY')
api_id = os.getenv('PLAY_HT_ID')

url = "https://play.ht/api/v1/convert"


def text_to_mp3(text_input):
    url = "https://play.ht/api/v1/convert"
    try:
        payload = {
            "content": [text_input],
            "voice": "en-US-JennyNeural"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "AUTHORIZATION": f"{api_key}",
            "X-USER-ID": f"{api_id}"
        }

        response = requests.post(url, json=payload, headers=headers)
        print('res:', response.text)
        response_dict = json.loads(response.text)
        transcription_id = response_dict['transcriptionId']
        if response_dict['status'] == "CREATED":
            # Download the MP3 file
            response = get_mp3_file(response_dict['transcriptionId'])
            old_data = get_data_api()
            new_data = {
                "gpt": {
                    "prompt_tokens": old_data['gpt']['prompt_tokens'],
                    "completion_tokens": old_data['gpt']['completion_tokens'],
                    "total_tokens": old_data['gpt']['total_tokens']
                },
                "deepai": old_data['deepai'],
                "dalle": old_data['dalle'],
                "playht": old_data['playht'] + response_dict['wordCount']
            }
            update_api_counter(new_data)
            return response
        else:
            # Stop the recursive return none
            print('text_to_mp3 ERR:', response.text)
            return None
    except Exception as e:
        time.sleep(10)
        get_mp3_file(response_dict['transcriptionId'])


def get_mp3_file(transcription_id):
    time.sleep(3)
    # Send GET request to Play.ht API to get MP3 file
    url = f"https://play.ht/api/v1/articleStatus?transcriptionId={transcription_id}"

    headers = {
        "accept": "application/json",
        "AUTHORIZATION": f"{api_key}",
        "X-USER-ID": f"{api_id}"
    }

    response = requests.get(url, headers=headers).json()
    return response['audioUrl']
