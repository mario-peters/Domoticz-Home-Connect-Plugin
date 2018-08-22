# Basic Python Plugin Example
#
# Author: GizMoCuz
#
"""
<plugin key="Home-Connect" name="Home-Connect Plugin" author="Mario Peters" version="1.0.0" wikilink="https://github.com/mario-peters/Domoticz-Home-Connect-Plugin/wiki" externallink="https://github.com/mario-peters/Domoticz-Home-Connect-Plugin">
    <description>
        <h2>Home-Connect domoticz plugin</h2><br/>
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Dishwasher-Monitor supported</li>
        </ul>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>Username is the username which you use in the Home-Connect app</li>
            <li>Password is the password which you use in the Home-Connect app</li>
            <li>Scope is the scope of the devices according to the Home-Connect API (<a href="https://developer.home-connect.com/docs/authorization/scope">API Home-Connect</a>).
                <ul style="list-style-type:square">
                    <li>Dishwasher-Monitor (only supported at this moment</li>
                </ul>
            </li>
        </ul>
        <br/><br/>
    </description>
    <params>
        <param field="Username" label="Username" width="150px" required="true"/>
        <param field="Password" label="Password" width="150px" required="true"/>
        <param field="Mode1" label="Scope" width="150px" required="true">
            <options>
                <option label="Dishwasher-Monitor" value="Dishwasher-Monitor" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import json
import requests
import datetime
from sseclient import SSEClient
from requests.exceptions import HTTPError
#import threading
import multiprocessing
import traceback

BASEURL = "https://api.home-connect.com"
CLIENT_ID = "EB32287B74E25B85212E25C2A6A3793B48CB2B4361F74210102791582172B617"
HEADER = {"content-type": "application/x-www-form-urlencoded"}
APP_NAME = "Domoticz connection"

class BasePlugin:
    enabled = False
    access_token = ""
    token_expired = datetime.datetime.now()
    refresh_token = ""
    haId = ""
    dishwasher_thread = None

    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        tempScope = Parameters["Mode1"].lower()
        tempScope = tempScope.replace("dishwasher-monitor","")
        tempScope = tempScope.replace(" ","")
        if(tempScope == ""):
            self.enabled = True
            Domoticz.Heartbeat(30)
            connectHomeConnect(self,Parameters["Username"],Parameters["Password"],Parameters["Mode1"])
            #Create devices
            if len(Devices) == 0:
                Domoticz.Log("Create devices")
                #Domoticz.Image(Filename="Icons.zip").Create()
                #Domoticz.Debug("Image: "+str(Images["Home-Connect"].ID))
                Domoticz.Device(Name="Dishwasher-Monitor", Unit=1, TypeName="Text", Used=1).Create()
                Devices[1].Update(nValue=Devices[1].nValue,sValue=Devices[1].sValue,Image=Images["Home-Connect"].ID)
        else:
            Domoticz.Error("Scope not correctly set. Only Dishwasher-Monitor allowed")

    def onStop(self):
        Domoticz.Log("onStop called")
        #self.dishwasher_thread.terminate()

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        if self.enabled == True:
            Domoticz.Log(str(datetime.datetime.now())+" onHeartbeat called")
            header = {"Accept": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer "+self.access_token}
            if isTokenValid(self) != True:
                if refreshToken(self) != True:
                   connectHomeConnect(self,Parameters["Username"],Parameters["Password"],Parameters["Mode1"])

            if self.haId == "":
                gethaId(self)
            """ 
                if self.dishwasher_thread == None:
                    #self.dishwasher_thread = threading.Thread(name="Dishwasher-thread",target=openSSEConnection(self))
                    Domoticz.Log("start dishwasher_thread")
                    jobs = []
                    self.dishwasher_thread = multiprocessing.Process(target=openSSEConnection, args=(self,))
                    jobs.append(self.dishwasher_thread)
                    self.dishwasher_thread.start()
            """
            openSSEConnection(self)

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def openSSEConnection(self):
    url_SSEConnection = BASEURL + "/api/homeappliances/" + self.haId + "/events"
    header = {"Accept": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer "+self.access_token}
    try:
        messages = SSEClient(url_SSEConnection, headers=header)
        for msg in messages:
            Domoticz.Debug("message: [["+str(msg)+"]]")
            if len(str(msg)) > 0:
                json_items = json.loads(str(msg))
                for key_item, value_item in json_items.items():
                    for data in value_item:
                        key = ""
                        value = ""
                        for k in data:
                            Domoticz.Debug(k + " --> " + str(data[k]))
                            if k == "key":
                                key = data[k]
                            if k == "value":
                                value = data[k]
                        if (key != "") and (value != ""):
                            if key == "BSH.Common.Status.OperationState":
                                status = value.rpartition(".")[2]
                                Domoticz.Debug("status: "+status)
                                if Devices[1].sValue != status:
                                    Devices[1].Update(nValue=0,sValue=status)
                            if key == "BSH.Common.Option.RemainingProgramTime":
                                if Devices[1].sValue.startswith("Run") == True:
                                    remainingTimeInSeconds = int(value)
                                    if remainingTimeInSeconds > 0:
                                        remainingTime = datetime.datetime.now() + datetime.timedelta(seconds=remainingTimeInSeconds)
                                        Domoticz.Debug("remainingTime: "+str(remainingTime.strftime("%T")))
                                        sValueNew = "Run - "+remainingTime.strftime("%T")
                                        if Devices[1].sValue != sValueNew:
                                            Devices[1].Update(nValue=value,sValue=sValueNew)
                                    
                            
#    except Exception as e:
#        Domoticz.Error(traceback.format_exc())
    except HTTPError as httperror:
        Domoticz.Error(httperror.response.text)
    except Exception as e:
        Domoticz.Error(traceback.format_exc())


def gethaId(self):
    url_homeappliances = BASEURL + "/api/homeappliances"
    header = {"Accept": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer "+self.access_token}
    response_homeappliances = requests.get(url_homeappliances, headers=header)
    Domoticz.Debug(response_homeappliances.text)
    json_homeappliances = json.loads(response_homeappliances.text)
    for key_homeappliance, value_homeappliance in json_homeappliances.items():
        Domoticz.Log(key_homeappliance + " --> " + str(value_homeappliance))
        homeappliance = value_homeappliance
        for data in homeappliance:
            items = homeappliance[data]
            for item in items:
                for key in item:
                    Domoticz.Debug(key + " --> " + str(item[key]))
                    if key == "haId":
                        self.haId = item[key]
                        Domoticz.Debug(self.haId)
    return

def isTokenValid(self):
    if datetime.datetime.now() < self.token_expired:
        return True
    return False

def refreshToken(self):
    url_refresh_token = BASEURL + "/security/oauth/token"
    data_refresh_token = {"refresh_token": self.refresh_token, "grant_type": "refresh_token"}
    response_refresh_token = requests.post(url_refresh_token,data_refresh_token,HEADER)
    json_refresh_token = json.loads(response_refresh_token.text)
    self.access_token = ""

    self.refresh_token = ""
    for key, value in json_refresh_token.items():
        if key == "access_token":
            self.access_token = value
        if key == "expires_in":
            self.token_expired = datetime.datetime.now() + datetime.timedelta(seconds=value)
        if key == "refresh_token":
            self.refresh_token = value

    if (self.access_token == "") or (self.token_expired < datetime.datetime.now()) or (self.refresh_token == ""):
        return False
    return True

def connectHomeConnect(self,username,password,scope):
    #"Request authorization to access home appliance" and "Return device code, user code, verification uri, ..."
    url_authorization = BASEURL + "/security/oauth/device_authorization"
    scope = "IdentifyAppliance "+scope
    data_authorization = {"client_id": CLIENT_ID, "scope": scope}
    response_authorization = requests.post(url_authorization,data_authorization,HEADER)
    Domoticz.Debug(response_authorization.text)
    json_data_authorization = json.loads(response_authorization.text)
    device_code = ""
    verification_uri_complete = ""
    user_code = ""
    for key, value in json_data_authorization.items():
        #print key + " --> " + str(value)
        Domoticz.Debug(key + " --> " + str(value))
        if key == "device_code":
            device_code = value
        if key == "verification_uri_complete":
            verification_uri_complete = value
        if key == "user_code":
            user_code = value
    Domoticz.Debug(device_code)
    Domoticz.Debug(verification_uri_complete)
    Domoticz.Debug(user_code)

    #"Access verification URI on browser" is not needed. But directly "Enter user code, log in and authorize access"
    authorized = False
    if(device_code != "") and (verification_uri_complete != "") and (user_code != ""):
        session = requests.Session()
        #response_verification_uri_complete = session.get(verification_uri_complete)
        #Domoticz.Debug(response_verification_uri_complete.text)

        #log in part
        payload_login = {"client_id": CLIENT_ID, "user_code": user_code, "email": username, "password": password}
        url_login = BASEURL + "/security/oauth/device_login"
        response_login = session.post(url_login, data=payload_login)
        Domoticz.Debug(response_login.text)
        sessionid = response_login.text[response_login.text.find("session_id\" value=\"")+len("session_id\" value=\""):]
        sessionid = sessionid[:sessionid.find("\"")]
        Domoticz.Debug("sessionid: "+sessionid)

        #authorize part
        payload_grant = {"session_id": sessionid, "client_id": CLIENT_ID, "user_code": user_code, "email": username, "app_name": APP_NAME, "scope": scope}
        url_grant = BASEURL + "/security/oauth/device_grant"
        response_grant = session.post(url_grant, data=payload_grant)
        Domoticz.Debug(response_grant.text)
        authorized = True

    #Token request
    if authorized:
        Domoticz.Log("Device \"" + device_code + "\" is authorized by Home-Connect.")
        url_tokenrequest = BASEURL + "/security/oauth/token"
        payload_tokenrequest = {"grant_type": "device_code", "device_code": device_code, "client_id": CLIENT_ID}
        response_tokenrequest = requests.post(url_tokenrequest,payload_tokenrequest,HEADER)
        Domoticz.Debug(response_tokenrequest.text)
        json_tokenrequest = json.loads(response_tokenrequest.text)
        for key, value in json_tokenrequest.items():
            Domoticz.Debug(key + " --> " + str(value))
            if key == "access_token":
                self.access_token = value
            if key == "expires_in":
                self.token_expired = datetime.datetime.now() + datetime.timedelta(seconds=value) #default 86400 seconds (=24h)
            if key == "refresh_token":
                self.refresh_token = value
        Domoticz.Log("Device\"" + device_code + "\" has token: " + self.access_token)
    else:
        Domoticz.Error("Device \"" + device_code + "\" is not authorized by Home_Connect.")

    return
