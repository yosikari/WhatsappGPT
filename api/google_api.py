import os
import json
import google.cloud.texttospeech as tts
from dotenv import load_dotenv
from google.auth import identity_pool
import json
from types import SimpleNamespace
from google.oauth2 import service_account
from google.cloud import storage
import requests
import cloudinary
from cloudinary.uploader import upload
from pydub import AudioSegment


load_dotenv()

credentials = service_account.Credentials.from_service_account_file(
    'env/whatsapp-gpt-384811-5c00af466b60.json')

# speed can be 0.25 to 4.0
speed = 1


def text_to_wav(voice_name: str, text: str):
    credential_str = credentials
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16, speaking_rate=speed)
    client = tts.TextToSpeechClient(credentials=credential_str)

    try:
        response = client.synthesize_speech(
            input=text_input,
            voice=voice_params,
            audio_config=audio_config,
        )
    except Exception as e:
        print('GOOGLE text_to_wav err:', e)

    filename = f"{voice_name}.wav"
    if not os.path.exists('sounds'):
        os.makedirs('sounds')

    with open(f'sounds/{filename}', 'wb') as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "sounds/{filename}"')

    convert_wav_to_mp3(f"sounds/{filename}")

    url = upload_wav_file_to_cloudinary(f"mp3/yossi.mp3")

    return url


def upload_wav_file_to_cloudinary(local_file_path):
    # Set up Cloudinary credentials
    cloudinary.config(
        cloud_name='dcqcatktj',
        api_key=os.getenv('UPLOAD_KEY'),
        api_secret=os.getenv('UPLOAD_SECRET')
    )

    # Upload local MP3 file to Cloudinary and get URL
    response = upload(local_file_path, resource_type="auto")
    sound_url = response['secure_url']

    # Return the sound URL
    return sound_url


def convert_wav_to_mp3(wav_path):
    sound = AudioSegment.from_wav(wav_path)
    sound.export('mp3/yossi.mp3', format="mp3")
