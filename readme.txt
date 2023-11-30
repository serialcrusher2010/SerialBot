Description:

This Twitch TTS Bot is two application. The first application is the bot itself.
The second application is the bot backend. The back is based on FastAPI and needed
to store the voice profiles for chatters in the channel.  

They do not need to be installed on the same computer.  

Instructions:


-- SerialBot Installation --
Copy the 'SerialBot' folder to the computer where the bot will run.  
In the folder is a requirements.txt file.  This is needed to install
all of the dependancies for the bot.  

If Python with pip is installed on the computer run the follow command in the SerialBot
folder:

python -m pip install -r requirements.txt

Then the bot can be ran from the commandline using:

python SerialBot.py

--SerialBot Back End Installation--
Copy the 'SerialBotBackEnd' folder to the computer where the backend will run.
In the folder is a requirements.txt file.  This is needed to install
all of the dependancies for the back end.

If Python with pip is installed on the computer run the follow command in the 
SerialBotBackEnd folder:

python -m pip install -r requirements.txt

Then the backend can be ran from the commandline using:

python -m uvicorn chatBotBackEnd:app --host 0.0.0.0 --port 8000 --reload


Each application has a .env.example file. This is where detials specific to your
Twitch and Google authenication is setup. All of the information is required for
the bot and backend to function. Once the information is entered in to the example
file save the name of the file as  .env

SerialBot:

TMI_TOKEN=oauth: This is your Twitchstream Key
CLIENT_ID= This is your bot application key
BOT_NICK= This is your bots nickname
BOT_PREFIX=!  This is the prefix that can be used for chatcommands
CHANNEL=  this is your TwitchName with a # in front of it
BROADCASTER= This is your TwitchName
SAFILE = '' THis is the path to your Google .json file that contains your auth token info
BACKENDSVR='' This is the IP to the backend 

SerialBotBackEnd:

TMI_TOKEN=oauth: This is your Twitchstream Key
CLIENT_ID= This is your bot application key
BOT_NICK= This is your bots nickname
BOT_PREFIX=!  This is the prefix that can be used for chatcommands
CHANNEL=  this is your TwitchName with a # in front of it
BROADCASTER= This is your TwitchName
SAFILE = '' THis is the path to your Google .json file that contains your auth token info
BACKENDSVR='' This is the IP to the backend





