import os
import requests

API_KEY = os.getenv('DEEPAI_KEY')


def deepaiRequest(prompt):
    prompt = prompt[3:len(prompt)]
    try:
        r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                'text': prompt,
            },
            headers={'api-key': API_KEY}
        ).json()
        print(r['output_url'])
        return {
            'response': str(r['output_url'])
        }
    except Exception as e:
        print('Text err:', e)
        return ('*DeepAi err:*'+e)
