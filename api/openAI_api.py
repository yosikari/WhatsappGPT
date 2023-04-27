from services.user_service import get_user, update_user_counter, add_user_note, clear_user_note, get_user_notes
from services.data_api_service import update_api_counter, get_data_api
from api.deepai_api import deepaiRequest
from pydub import AudioSegment
from io import BytesIO
import requests
import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

currUser = ''


def voice_trascript(voice):
    # Download the audio file from the URL
    audio_url = voice
    response = requests.get(audio_url)

    # Convert the audio from ogg to wav format
    audio_bytes = BytesIO(response.content)
    audio = AudioSegment.from_file(audio_bytes, format="ogg")
    audio.export("audio.wav", format="wav")

    # Read the audio file and transcribe it using OpenAI's
    audio_file = open("audio.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1",
                                         audio_file)

    # Output the transcription
    return (str(transcript.text))

    # Return response from GPT / Dall-E / Custom commends
    # -----Commends:--
    # --/h--help------
    # --/u--user-usage
    # --/d--Dall-E-2--
    # --/m--Midjourney
    # --/s--Save------
    # --/l--List------
    # --/c--Clear-----
    # --/q--Question--
    # --/t-Translate
    # --/v-Text To Speech
    # --/w--Weather
    # --/api-Api-usage


def chat_complition(prompt: str, sender_id) -> dict:

    # Set current user
    global currUser
    currUser = sender_id
    user = get_user(currUser)

    # Return Dall-E-2
    if prompt[0:2] == '/d':
        if user['dalle'] != "0":
            update_user_counter(currUser, 'dalle', str(int(user['dalle'])-1))
            res = dallE2Request(prompt)
            return res
        else:
            return {
                'response': ("Sorry,\n\nYour Dall-E-2 free trial is over,\nhope you enjoyed it.\n\n*Free trail stats:*\nChat GPT (<text>): *"+user['gpt']+"*\nDall-E-2 (/d <text>): *"+user['dalle']+"*\nMidjourney (/m <text>): *"+user['deepai']+"*\nWeather (/w or /w <city>): *Unlimited*\n\n/h for more info.")}

    # Return DeepAI
    elif prompt[0:2] == '/m':
        if user['deepai'] != "0":
            update_user_counter(currUser, 'deepai', str(int(user['deepai'])-1))
            res = deepaiRequest(prompt)
            old_data = get_data_api()
            new_data = {
                "gpt": {
                    "prompt_tokens": old_data['gpt']['prompt_tokens'],
                    "completion_tokens": old_data['gpt']['completion_tokens'],
                    "total_tokens": old_data['gpt']['total_tokens']
                },
                "deepai": old_data['deepai']+0.05,
                "dalle": old_data['dalle'],
                "playht": old_data['playht']
            }
            update_api_counter(new_data)
            return res
        else:
            return {
                'response': ("Sorry,\n\nYour Midjourney free trial is over,\nhope you enjoyed it.\n\n*Free trail stats:*\nChat GPT (<text>): *"+user['gpt']+"*\nDall-E-2 (/d <text>): *"+user['dalle']+"*\nMidjourney (/m <text>): *"+user['deepai']+"*\nWeather (/w or /w <city>): *Unlimited*\n\n/h for more info.")}

    # Return commends list
    elif prompt[0:2] == '/h':
        return {
            'response': '*Commends:* \n \n /u - Check usage. \n \n <your text> - ChatGPT. \n \n /d <your text> - Dall-E-2. \n\n /m <your text> - Midjourney. \n \n /s <your text> - Save text. \n\n /q <your text> - Question from saved. \n\n /l - Show saved text. \n\n /c - Clear saved. \n\n /w - Weather (city name optional). \n\n /v <text> - Text to speech female English.\n\n /v en <text> - Text to speech male English.\n\n /v he <טקסט> - Text to speech Hebrew.\n\n /v he2 <טקסט> - Text to speech female Hebrew.\n\n /v ru <text> - Text to speech Russian.\n\n /v ru2 <text> - Text to speech female Russian.\n\n /t <he> <text> - Translate. \n /t info - Translate languages. \n\n *You also can use voice msg*\n\nEvery new user will charge with:\nChatGPT *30* requests,\nDall-E-2 *3* requests,\nMidjourney *3* requests,\nWeather *Unlimited*.\n\n *Credits:* \n Created by yosikari, \n https://yossikarasik.com \n\n https://www.youtube.com/watch?v=JiPVyhliryw'}

    # Return user stats
    elif prompt[0:2] == '/u':
        return {
            'response': ("*"+currUser+" Stats:*\n(how much left on my trial)\n\nChat GPT (<text>): *"+user['gpt']+"*\nDall-E-2 (/d <text>): *"+user['dalle']+"*\nMidjourney (/m <text>):*"+user['deepai'])+"*\nText to speech (/v <text>):*"+user['playht']+"*\nWeather (/w or /w <city>): *Unlimited*\n\n/h for more info."}

    # Save prompt (update 'saved' variable)
    elif prompt[0:2] == '/s':
        end = len(prompt)
        add_user_note(currUser, prompt[3:end])
        return {
            'response': (prompt[3:end] + '\n \n *Successfully saved.*')}

    # Return saved data (from 'saved' variable)
    elif prompt[0:2] == '/l':
        data = get_user_notes(currUser)
        result = ""
        for key, value in data.items():
            result += f"{key} : {value} ,\n\n"
        if (result == ""):
            return {
                'response': ('*You have not saved data.*')}
        else:
            return {
                'response': ('*Saved data:*'+'\n \n'+result)}

    # Clear saved data (from 'saved' variable)
    elif prompt[0:2] == '/c':
        clear_user_note(currUser)
        return {
            'response': ('*Successfully cleared saved data.*')}

    # Return open-ai and midjourney api usage data
    elif prompt[0:4] == '/api':
        data = get_data_api()
        result = ""
        for key, value in data.items():
            result += f"{key} : {value} ,\n"

        return {
            'response': ('*API usage:* \n *ChatGPT:*\n prompt_tokens: ' + str(format(data['gpt']['prompt_tokens'], ','))+'\n completion_tokens: '+str(format(data['gpt']['completion_tokens'], ','))+'\n total_tokens: '+str(format(data['gpt']['total_tokens'], ','))+'\n Total: '+str(round(data['gpt']['total_tokens']*0.000002, 3))+' $\n\n *Dall-E-2:*\n Total: '+str(round(data['dalle'], 3))+' $\n\n *Midjourney:*\n Total:  '+str(round(data['deepai'], 3))+' $\n\n'+' *PlayHT:*\n Total: '+str(5000-data['playht']) + ' words left.\n\n'+'*Total:* *'+str("{:.3f}".format((data['gpt']['total_tokens']*0.000002)+data['deepai']+data['dalle']))+' $*')}


# Return translate
    elif prompt.startswith('/t') and not prompt.startswith('/t info'):
        end = len(prompt)
        text = prompt[2:end]
        lang_map = {
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ar": "Arabic",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "hi": "Hindi",
            "bn": "Bengali",
            "ru": "Russian",
            "uk": "Ukrainian",
            "pl": "Polish",
            "cs": "Czech",
            "sk": "Slovak",
            "hu": "Hungarian",
            "ro": "Romanian",
            "hr": "Croatian",
            "he": "Hebrew",
            "sr": "Serbian",
            "sl": "Slovenian",
            "mk": "Macedonian",
            "bg": "Bulgarian",
            "el": "Greek",
            "tr": "Turkish",
            "fa": "Persian"
        }

        lang_code = prompt[3:5]
        lang_name = lang_map.get(lang_code, 'English')
        text = prompt[6:] if lang_name != 'English' else prompt[3:]
        res = chatGptRequest(f"Translate to {lang_name}: {text}")
        return res

    # Return translate info
    elif prompt.startswith('/t info'):
        text = "*Translate codes:*\n\nempty: English,\n" \
            "es: Spanish,\n" \
            "fr: French,\n" \
            "de: German,\n" \
            "it: Italian,\n" \
            "pt: Portuguese,\n" \
            "ar: Arabic,\n" \
            "zh: Chinese,\n" \
            "ja: Japanese,\n" \
            "ko: Korean,\n" \
            "hi: Hindi,\n" \
            "bn: Bengali,\n" \
            "ru: Russian,\n" \
            "uk: Ukrainian,\n" \
            "pl: Polish,\n" \
            "cs: Czech,\n" \
            "sk: Slovak,\n" \
            "hu: Hungarian,\n" \
            "ro: Romanian,\n" \
            "hr: Croatian,\n" \
            "he: Hebrew,\n"\
            "sr: Serbian,\n" \
            "sl: Slovenian,\n" \
            "mk: Macedonian,\n" \
            "bg: Bulgarian,\n" \
            "el: Greek,\n" \
            "tr: Turkish,\n" \
            "fa: Persian."

        return {
            'response': text
        }
    # Return answer from saved data (from user notes data)
    elif prompt[0:2] == '/q':
        data = get_user_notes(currUser)
        result = ""
        for key, value in data.items():
            result += f"{key} : {value} ,\n\n"
        qprompt = ('Answer only from this text: ' + result + '. Question: \n' + prompt[3:len(prompt)] + '\n If there is no text provided, just answer: \'You don\'t have saved reminders use /s to save reminders, and try agine\'.'
                   )
        if user['gpt'] != "0":
            update_user_counter(currUser, 'gpt', str(int(user['gpt'])-1))
            res = chatGptRequest(qprompt)
            return res
        else:
            return {
                'response': ("Sorry,\n\nYour GPT free trial is over,\nhope you enjoyed it.\n\n*Free trail stats:*\nChat GPT (<text>): *"+user['gpt']+"*\nDall-E-2 (/d <text>): *"+user['dalle']+"*\nMidjourney (/m <text>): *"+user['deepai']+"*\nWeather (/w or /w <city>): *Unlimited*\n\n/h for more info.")
            }
    # Return answer from GPT-3.5
    else:
        if user['gpt'] != "0":
            update_user_counter(currUser, 'gpt', str(int(user['gpt'])-1))
            res = chatGptRequest(prompt)
            return res
        else:
            return {
                'response': ("Sorry,\n\nYour GPT free trial is over,\nhope you enjoyed it.\n\n*Free trail stats:*\nChat GPT (<text>): *"+user['gpt']+"*\nDall-E-2 (/d <text>): *"+user['dalle']+"*\nMidjourney (/m <text>): *"+user['deepai']+"*\nWeather (/w or /w <city>): *Unlimited*\n\n/h for more info.")}


def dallE2Request(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt[3:len(prompt)],
            n=1,
            size="1024x1024",
        )

        old_data = get_data_api()
        new_data = {
            "gpt": {
                "prompt_tokens": old_data['gpt']['prompt_tokens'],
                "completion_tokens": old_data['gpt']['completion_tokens'],
                "total_tokens": old_data['gpt']['total_tokens']
            },
            "deepai": old_data['deepai'],
            "dalle": old_data['dalle']+0.02,
            "playht": old_data['playht']
        }
        update_api_counter(new_data)
        return {
            'response': (response["data"][0]["url"])
        }
    except Exception as e:
        print('error dele', e)
        return {
            'response': ('*Dall-E-2 ERROR:* '+str(e))
        }


def chatGptRequest(prompt):
    global prompt_tokens
    global completion_tokens
    global total_tokens
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt},
            ])
        prompt_tokens = response['usage']['prompt_tokens']
        completion_tokens = response['usage']['completion_tokens']
        total_tokens = response['usage']['total_tokens']
        old_data = get_data_api()

        new_data = {
            "gpt": {
                "prompt_tokens": (old_data['gpt']['prompt_tokens']+prompt_tokens),
                "completion_tokens": (old_data['gpt']['completion_tokens']+completion_tokens),
                "total_tokens": (old_data['gpt']['total_tokens']+total_tokens)
            },
            "deepai": old_data['deepai'],
            "dalle": old_data['dalle'],
            "playht": old_data['playht']
        }

        update_api_counter(new_data)
        return {
            'response': response['choices'][0]['message']['content']
        }
    except Exception as e:
        print('GPT ERROR:', e)
        return {'response': ('*Failed to get GPT answer, please try agine later, ERR CODE:* '+str(e))}
