<h2>WhatsappGPT</h2>

<img src="/readme-img/03.jpg" width="600"/>

## Project Features
This is a simple python script, that allow the user to send whatsapp question massage to twilio sandbox number, and receive answers from chatGPT AI.

## Demo:
Run this whatsapp command 'join run-pack'
to flowing whatsapp phone number: '+14155238886'

- You should get this response massage: 
<img src="/readme-img/01.jpg" height="600"/>

- Then you can ask any question from the assistance bot:
<img src="/readme-img/02.jpg" height="600"/>

Note: This is demo demonstration only,
After several attempts you will be blocked.

<h2>Libraries Used</h2>
<b>This project is using the following libraries:
</b>

- [`Flask`](https://flask.palletsprojects.com/en/2.2.x/)

- [`openAI`](https://platform.openai.com/docs/libraries)

- [`Twilio`](https://www.twilio.com/docs/libraries/python)

## Installation
To run the project locally, follow these steps:

Clone the repository: 
`git clone https://github.com/yosikari/WhatsappGPT.git`

Install dependencies: 
`pip install Flask openai python-dotenv twilio`

Open '.env' file and configure your api keys:

- 'OPENAI_API_KEY' = [`Can get yours key here`](https://platform.openai.com/account/api-keys) 
- 'TWILIO_SID' = [`Can get yours key here`](https://www.twilio.com/docs/glossary/what-is-a-sid) 
- 'TWILIO_TOKEN' = [`Can get yours key here`](https://www.twilio.com/en-us) 

Then get your whatsapp phone number from [`Twilio`]() ,  
Configure the number on 'twilio_api.py' file,
use the web hook url: 'BASEURL/twilio/receiveMessage', 
on your twilio path: Develop/Messaging/Send a WhatsApp message / Sandbox settings
<img src="/readme-img/04.jpg"/>

Now you can connect to sandbox by sending `join <sandbox name>`

## Contact Me
If you have any questions or feedback about the project, please feel free to reach me out at yosikari@gmail.com.
