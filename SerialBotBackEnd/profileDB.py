import pickle
import json

class profileDB:

    def __init__(self, filename):
        self.listOfProfiles = []
        self.filename = filename
        self.loadDB()
        self.savedSinceLastChange = False
        
    def loadDB(self):
        try:
            with open(self.filename, 'rb') as f:
                self.listOfProfiles = pickle.load(f)
                print ('DB opened')
                return 'DB opened1'
        except:
            self.saveDB()
            print(self.filename + " doesn't exist. Creating Empty DB")
            return self.filename + " doesn't exist. Creating Empty DB"

    def saveDB(self):
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.listOfProfiles, f)
            self.savedSinceLastChange = True
            print("Saving DB")
        except:
            print ("Error opening profile db " + self.filename)
            return "Error opening profile db " + self.filename

    def createProfile(self, Name: str="None", Nick: str="None"):
        index = self.__getProfileIndex(Name)
        if(index != -1):
            print("Profile for " + Name + " already exists")
            return "Profile for " + Name + " already exists"
        try:
            if(Name == "None"):
                return "Name Must be entered"
            else:
                if(Nick == "None"):
                    self.listOfProfiles.append(profileListItem(Name, Name))
                else:
                    self.listOfProfiles.append(profileListItem(Name, Nick))
            self.savedSinceLastChange = False
            print("Profile Created for " + Name)
            return "Profile Created for " + Name

        except:
            print("Unable to create profile for " + Name)
            return "Unable to create profile for " + Name
    
    def modifyProfile(self, item):
        self.deleteProfile(item.name)
        self.listOfProfiles.append(item)
        return 0

    def deleteProfile(self, Name: str="none"):
        index = self.__getProfileIndex(Name)
        if(index == -1):
            print("Profile for " + Name + " doesn't exists")
            return "Profile for " + Name + " doesn't exists"
        if(Name == "None"):
            return "Name Must be entered"
        else:
            self.listOfProfiles.pop(index)
            self.savedSinceLastChange = False
            print("Profile Deleted for " + Name)
            return "Profile Deleted for " + Name
        
        try:
            print('')
        except:
            print("Unable to delete profile for " + Name)
            return "Unable to delete profile for " + Name

    def debugPrintProfileList(self):
        for p in self.listOfProfiles:
            print(p.name)
            print(p.nick)
            print(p.usesGCTTS)
            print(p.gcLangCode)
            print(p.gcSSMLGender)
            print(p.gcName)
            print(p.msVoice)

    def getProfileList(self):
        return self.listOfProfiles

    def __getProfileIndex(self, Name: str="None"):
        if(Name == "None" or Name == ""):
            print("Please enter a name")
            return "Please enter a name"
        else:
            index = -1
            idx = 0
            
            for p in self.listOfProfiles:
                if p.name == Name:
                    index = idx
                    break
                idx = idx + 1
            #Will return -1 if profile not found
            return index 

class profileListItem:
    def __init__(self, name: str='', nick: str=''):
        self.name = name
        self.nick = nick
        self.usesGCTTS = False
        self.gcLangCode = ""
        self.gcSSMLGender = ""
        self.gcName = ""
        self.msVoice = ""
        self.voiceChanged = False
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


