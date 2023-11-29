import os, sys
import pyttsx3
import random
import pickle
import requests, json
from threading import Timer

from google.cloud import texttospeech
from google.oauth2 import service_account
import winsound

from twitchio.ext import commands, eventsub
from dotenv import load_dotenv

# TODO:
# Add Commands to modify Chatter Profile Settings
# Implement 'simple' rest API
# Implement save feature for settings
# In Message Event Create Function defines for all sections
# Add functionality to make coffee
# Add Speech Translation
# Give bot a dino body

tts = pyttsx3.init()
tts.setProperty('rate', 200)

#Generate List of Available MS Voices
voiceListMS = tts.getProperty('voices')
numMSVoices = len(voiceListMS)
load_dotenv()

safile=str(os.environ['SAFILE'])

usesOfflineMode = os.environ['OFFLINE_MODE']

#Authenticate to Google Cloud (GC) TTS
#**Add safile variable to ENV settings file
credentials = service_account.Credentials.from_service_account_file(safile)
client = texttospeech.TextToSpeechClient(credentials=credentials)
#Generate List of Available GC Voices
request = texttospeech.ListVoicesRequest()
voiceListGC = client.list_voices(request=request).voices
numGCVoices = len(voiceListGC)

print(numGCVoices)

class profileListItem:
    def __init__(self, name, nick):
        self.name = name
        self.nick = nick
        self.usesGCTTS = False
        self.voiceMSID = random.randint(0, numMSVoices - 1)
        self.voiceGCTTS = random.randint(0, numGCVoices - 1)

listOfProfiles = []

class msTTSProfile:
    def __init__(self):
        self.voice = 0
        self.rate = 200

try:
    with open('profileList.lst', 'rb') as f:
        listOfProfiles = pickle.load(f)
except:
    print("profileList.lst doesn't exist.")

#Add to .ENV Later    
replacements = {'_': ' ', '-': ' '}

bot = commands.Bot(
    token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

backEndSVR = os.environ['BACKENDSVR']

print('Back end Server addr: ', backEndSVR)

tts.say(os.environ['BOT_NICK'] + " is running")
tts.runAndWait()

print (os.environ['BOT_NICK'] + " is active in " + os.environ['CHANNEL'])

def TestConnection():
    global chatBotConnected
    Timer(60, TestConnection).start()
    resp = requests.get(backEndSVR +'/testRestConnection')
    print('Connected to backend present: ', resp)
    
TestConnection()

@bot.event()
async def event_message(data):
    global usesOfflineMode

    userName = data.author.display_name
    userSaid = data.content
    userIsMod = data.author.is_mod
    userIsBroadcaster = data.author.is_broadcaster

    data = json.dumps({'name': userName})
    resp = requests.post(backEndSVR + '/getUserProfile', data)

    print(resp.json())

    jsonObj = json.loads(resp.json())
    name = jsonObj["nick"]
    
    if(name == "noneBlankdefault"):
        name = userName
        replaced_chars = [replacements.get(char, char) for char in name] 
        pronounced_name = ''.join(replaced_chars)
        msg = pronounced_name + " said " + userSaid
        msgOut = userName + ": " + userSaid 
        print(msgOut)
        GCTTSsay(msg, jsonObj)
    else:
        replaced_chars = [replacements.get(char, char) for char in name] 
        pronounced_name = ''.join(replaced_chars)
        msg = pronounced_name + " said " + userSaid
        msgOut = userName + ": " + userSaid 
        print(msgOut)
        GCTTSsay(msg, jsonObj)

def getVoiceGender(gender):
    match gender:
        case 'undefined':
            return 0
        case 'male':
            return 1
        case 'female':
            return 2
        case 'neutral':
            return 3

def GCTTSsay(msg, person):
    print(person)    
    useLangCode = person['gcLangCode']
    useSSMLGender = getVoiceGender(person['gcSSMLGender'])
    useName = person['gcName']
    
    synthesis_input = texttospeech.SynthesisInput(text=msg)
    
    voice = texttospeech.VoiceSelectionParams(
        #language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.FEMALE, name='en-US-Neural2-G'
        language_code=useLangCode, ssml_gender=useSSMLGender, name=useName
        )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)

    winsound.PlaySound(response.audio_content, winsound.SND_MEMORY)

def MSTTSSay(msg, chatterIDX):
    voice = getMSVoiceInfo(chatterIDX).id
    tts.setProperty('voice', voice)
    tts.say(msg)
    tts.runAndWait()

if __name__ == "__main__":
    bot.run()




        
