import json, os, atexit
from threading import Timer, enumerate
 
from profileDB import profileDB, profileListItem

from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account

load_dotenv()
safile=str(os.environ['SAFILE'])
app = FastAPI()

app.mount("/asset", StaticFiles(directory="asset"), name='asset')

credentials = service_account.Credentials.from_service_account_file(safile)
client = texttospeech.TextToSpeechClient(credentials=credentials)
#Generate List of Available GC Voices
request = texttospeech.ListVoicesRequest()
voiceListGC = client.list_voices(request=request).voices
numGCVoices = len(voiceListGC)
print ("Number of GC Voices: "  + str(numGCVoices))

chatBotConnected = False
mytimer = ""

def resetTestConnection():
    global mytimer
    global chatBotConnected
    mytimer = Timer(300, resetTestConnection )
    mytimer.start()
    mytimer.name = "myTimerThread"
    chatBotConnected = False

resetTestConnection()

def exit_handler():
    print('atexit exit_handler')
    
atexit.register(exit_handler)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = profileDB('profileDatabase.db')

@app.on_event("startup")
def startup():
    print("FastAPI Starting")

@app.on_event("shutdown")
def shutdown():
    global mytimer
    print("Shutting it down")
    mytimer.cancel()
    mytimer.join()
            
@app.get("/")
def default():
    file = r'html\index.html'
    with open(file) as fh:
        data = fh.read()
    return HTMLResponse(data)

@app.post("/createProfile")
async def createProfile(request: Request):
    x = await request.json()
    Name = x['name']
    if(Name == 'none'):
        return 'No Name Entered'
    else:
        print('Created profile for: ' + Name)
        db.createProfile(Name, Name)
        db.saveDB()
        return "Created profile for: " + Name

@app.post("/modifyProfile")
async def modifyProfile(request: Request):
    p = profileListItem()
    x = await request.json()
    p.name = x['name']
    p.nick = x['nick']
    p.usesGCTTS = x['usesGCTTS']
    p.gcLangCode = x['gcLangCode']
    p.gcSSMLGender = x['gcSSMLGender']
    p.gcName = x['gcName']
    db.modifyProfile(p)
    db.saveDB()

@app.delete("/deleteProfile")
async def deleteProfile(request: Request):
    x = await request.json()
    Name = x['name']
    if(Name == 'none'):
        return 'No Name Entered'
    else:
        print('Deleted profile for: ' + Name)
        db.deleteProfile(Name)
        db.saveDB()
        return "Deleted profile for: " + Name

@app.get("/getUserProfileNames")
def userProfileNames():
    pList = db.getProfileList()
    nList = []
    for p in pList:
        nList.append(p.name)
    data = json.dumps(nList)
    return JSONResponse(data)

@app.post('/getUserProfile')
async def getUserProfile(request: Request):
    x = await request.json()
    name = x['name']
    pList = db.getProfileList()
    print('retriving data for: ', name)
    for p in pList:
        if (p.name == name):
            data = p.toJSON()
            print("0:", data)
            return data

    #Add this to future bot settings update
    return '{"nick": "noneBlankdefault" , "gcLangCode": "en-US", "gcName": "en-US-Wavenet-C", "gcSSMLGender": "female", "usesGCTTS", true}'
    
@app.get("/getGCVoicesList")
def getGCVoiceList():
    global voiceListGC
    vJson = getVoiceListJson(voiceListGC)
    return vJson

@app.get("/testRestConnection")
def testRestConnection():
    global chatBotConnected
    chatBotConnected = True
    return True

@app.get("/isChatBotConnected")
def isChatBotConnected():
    global chatBotConnected
    if (chatBotConnected == True):
        return 'true'
    else:
        return 'false'

@app.get("/getSystemStatus")
def getSystemStatus():
    global chatBotConnected
    global numGCVoices
    profiles = db.getProfileList()

    if(chatBotConnected):
        cbconnected = 'True'
    else:
        cbconnected = 'False'

    jsonObj = {
        "Cbconnected": cbconnected,
        "numGCVoices": numGCVoices,
        "numProfiles": len(profiles)

    }

    return json.dumps(jsonObj)

def getProfileListItemObjFromDict(dict):
    try:
        pItem = profileListItem('','')
        pItem.name = dict['name']
        pItem.nick = dict['nick']
        pItem.usesGCTTS = dict['usesGCTTS']
        pItem.gcLangCode = dict['gcLangCode']
        pItem.gcSSMLGender = dict['gcSSMLGender']
        pItem.gcName = dict['gcName']
        pItem.msVoice = dict['msVoice']
        pItem.voiceChanged = dict['voiceChanged']
        return pItem
    except Exception as error:
        print("Error in def getProfileListItemObjFromDict: " + error )

def getVoiceListJson(voiceList):
    output = "["
    for voice in voiceListGC:
        item = voiceListItem(voice.name, voice.ssml_gender, voice.language_codes[0], voice.natural_sample_rate_hertz)
        output = output + item.toJSON() + ','
    output = output[:-1] + "]"
    return JSONResponse(output)

class voiceListItem:
    def __init__(self, voiceName, voiceGender, voiceLangCode, sampleRate):
        self.voiceName = voiceName
        self.voiceGender = voiceGender
        self.voiceLangCode = voiceLangCode
        self.voiceSampleRate = sampleRate
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    


