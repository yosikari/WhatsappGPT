<h2>WhatsappGPT</h2>

<img src="/readme-img/03.jpg" width="600"/>

[<img src="/readme-img/youtube.jpeg" width="600"/>](https://youtu.be/JiPVyhliryw)

## Project Features
This is a simple python script, that allow the user to send whatsapp question massage to twilio sandbox number, and receive answers from ChatGPT, Dall-E-2, Midjourney (based on deepai.org), OpenWeather, Save notes, ask questions based on notes, and more awesome fetchers.

## Demo:
Run this whatsapp command 'join run-pack'
to flowing whatsapp phone number: '+14155238886'

- You should get this response massage: 
<img src="/readme-img/01.jpg" height="600"/>

- Then you can just send 'Hi' and the assistance bot will register you automatically:
<img src="/readme-img/join.jpg" height="600"/>

Note: This is a demo demonstration only,
each user gets a free trail of 30 ChatGPT requests, 3 Dall-E-2 requests and 3 Midjourney requests.

<h2>Chat Commends:</h2>

`/h` - Help.

`/u` - User usages, show how many requests are left in each category.

`/d <text>` - Dall-E-2, an image will be generated based on your input using Dall-E-2 API.

`/m <text>` - Midjourney, an image will be generated based on your input using Midjourney API. 

`/s <text>` - Save, your input will be saved to a user session notes (the saved notes can be viewed or cleared)

`/l` - List, view your saved notes.

`/c` - Clear, will delete your saved notes.

`/q <text>` - Question, will answer your question based on your saved notes.

`/t <lang-code> <text>` - Translate, will translate your input to your selected language (28 language codes).

`/t info` - Return supported languages list.

`/v <lang-code> <text>` - TTS test to speech, return voice message of the text input (langs code he , he2 , ru , ru2 , en2 , empty - default language English female.)

`/w | Optional <city>` - get the weather in the requested city, the default city is 'Tel Aviv'.

`/api` - For developers - will calculate your api total usage and cost from all users.

You also can send voice messages, ChatGpt will transcript your message, and then answer it.

<b>It's also support any language.</b>

You can take a look at comments use on the [Gallery](#Gallery)


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
- 'TWILIO_SID' = [`Can get yours sid here`](https://www.twilio.com/docs/glossary/what-is-a-sid) 
- 'TWILIO_TOKEN' = [`Can get yours token here`](https://www.twilio.com/en-us)
- 'DEEPAI_KEY' = [`Can get yours key here`](https://deepai.org/) 
- 'OPEN_WEATHER_KEY' = [`Can get yours key here`](https://openweathermap.org/) 

- 'PLAY_HT_ID' = [`Can get yours id here`](https://play.ht/)

- 'PLAY_HT_KEY' = [`Can get yours key here`](https://play.ht/)

- 'UPLOAD_KEY' = Cloudinary
- 'UPLOAD_SECRET' = Cloudinary

<b>Note: for google TTS you have to setup google credentials json file and add it to env path.</b>

Then get your whatsapp phone number from [`Twilio`]() ,  
Configure the number on 'twilio_api.py' file,
use the web hook url: 'BASEURL/twilio/receiveMessage', 
on your twilio path: Develop/Messaging/Send a WhatsApp message / Sandbox settings
<img src="/readme-img/04.jpg"/>

Now you can connect to sandbox by sending `join <sandbox name>`

## Contact Me
If you have any questions or feedback about the project, please feel free to reach me out at yosikari@gmail.com.


## Gallery

#### Join the sandbox
<img src="/readme-img/join.jpg" width="420"/>

#### User usage
<img src="/readme-img/u.jpg" width="420"/>

#### Commends list
<img src="/readme-img/h.jpg" width="420"/>

#### ChatGPT answer
<img src="/readme-img/gpt.jpg" width="420"/>

#### Dall-E-2 generate
<img src="/readme-img/d.jpg" width="420"/>

#### Midjourney generate
<img src="/readme-img/m.jpg" width="420"/>

#### Save notes
<img src="/readme-img/s.jpg" width="420"/>

#### Ask question based on notes
<img src="/readme-img/q.l.jpg" width="420"/>

#### Clear saved notes
<img src="/readme-img/c.l.jpg" width="420"/>

#### Weather
<img src="/readme-img/w.jpg" width="420"/>

#### Voice messages transcript and answered
<img src="/readme-img/voice.jpg" width="420"/>

#### TTS text to speech
<img src="/readme-img/tts.jpg" width="420"/>

#### Translate text
<img src="/readme-img/t.jpg" width="420"/>


#### Translate list of supported languages
<img src="/readme-img/tinfo.jpg" width="420"/>

#### Any language are supported
<img src="/readme-img/voice.he.jpg" width="420"/>

#### API usage and costs information 
<img src="/readme-img/api.jpg" width="420"/>
