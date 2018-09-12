import Domoticz
import datetime
import requests
import json
from sseclient import SSEClient
from requests.exceptions import HTTPError
import traceback

BASEURL = "https://api.home-connect.com"
HEADER_URLENCODED = {"content-type": "application/x-www-form-urlencoded"}
CLIENT_ID = "EB32287B74E25B85212E25C2A6A3793B48CB2B4361F74210102791582172B617"
APP_NAME = "Domoticz connection"

"""
Method for checking if a oauth2 token is still valid
 
Parameters
----------
self : BasePlugin
    for getting plugin variables
"""
def isTokenValid(self):
    if datetime.datetime.now() < self.token_expired:
        return True
    return False

"""
Method for refreshing the token after token is invalid (24 hours)

Parameters
----------
self : BasePlugin
    for getting plugin variables

Return values
-------------
True : Token correctly refreshed
False : Token not correctly refreshed
"""
def refreshToken(self):
    url_refresh_token = BASEURL + "/security/oauth/token"
    data_refresh_token = {"refresh_token": self.refresh_token, "grant_type": "refresh_token"}
    response_refresh_token = requests.post(url_refresh_token,data_refresh_token,HEADER_URLENCODED)
    json_refresh_token = json.loads(response_refresh_token.text)
    self.access_token = ""
    self.refresh_token = ""
    for key, value in json_refresh_token.items():
        if key == "access_token":
            self.access_token = value
        if key == "expires_in":
            self.token_expires = datetime.datetime.now() + datetime.timedelta(seconds=value)
        if key == "refresh_token":
            self.refresh_token = value

    if (self.access_token == "") or (self.token_expired < datetime.datetime.now()) or (self.refresh_token == ""):
        return False
    return True

"""
Method for getting the Home-Connect Appliance ID

Parameters
----------
self : BasePlugin
    for getting plugin variables

Return
------
None
"""
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

"""
Method for opening "Server Side Event"-tunnel to Home-Connect for getting status updates

Parameters
----------
self : BasePlugin
    for getting plugin variables

Return
------
None
"""
def openSSEConnection(self, Devices):
    Domoticz.Log("openSSEConnection")
    url_SSEConnection = BASEURL + "/api/homeappliances/" + self.haId + "/events"
    header = {"Accept": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer " + self.access_token}
    try:
        messages = SSEClient(url_SSEConnection, headers=header)
        for msg in messages:
            Domoticz.Debug("message: [[" + str(msg) + "]]")
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
                            if key == "BSH.Common.Root.SelectedProgram":
                                Domoticz.Log(key + " --> " + str(value).rpartition(".")[2])
                                self.selectedprogram = value.rpartition(".")[2]
                            #if key == "BSH.Common.Root.ActiveProgram":
                                #Domoticz.Log(key + " --> " + str(value))
                            if key == "BSH.Common.Option.RemainingProgramTime":
                                if Devices[1].sValue.startswith("Run") == True:
                                    remainingTimeInSeconds = int(value)
                                    if remainingTimeInSeconds > 0:
                                        remainingTime = datetime.datetime.now() + datetime.timedelta(seconds=remainingTimeInSeconds)
                                        Domoticz.Debug("remainingTime: " + str(remainingTime.strftime("%H:%M")))
                                        sValueNew = "Run - " + remainingTime.strftime("%H:%M")
                                        if Devices[1].sValue != sValueNew:
                                            Devices[1].Update(nValue=value,sValue=sValueNew)
                            if key == "BSH.Common.Option.ProgramProgress":
                                Domoticz.Log(key + " --> " + str(value))
                                sValueNew = Devices[1].sValue
                                Domoticz.Log("sValueNew: "+sValueNew)
                                if self.selectedprogram == "PreRinse":
                                    if sValueNew.count('_Run') == 0:
                                        sValueNew = "rinse_"+sValueNew
                                    else:
                                        sValueNew = "rinse_"+sValueNew.split('_', 1)[1]
                                #if self.selectedprogram == "Quick45":
                                #if self.selectedprogram == "Glas40":
                                #if self.selectedprogram == "Kurz60":
                                #if self.selectedprogram == "NightWash":
                                if self.selectedprogram == "Eco50":
                                    if value > 0 and value < 10:
                                        if sValueNew.count('_Run') == 0:
                                            sValueNew = "rinse_"+sValueNew
                                        else:
                                            sValueNew = "rinse_"+sValueNew.split('_', 1)[1]
                                    if value >= 10 and value < 60:
                                        if sValueNew.count('_Run') == 0:
                                            sValueNew = "clean_"+sValueNew
                                        else:
                                            sValueNew = "clean_"+sValueNew.split('_', 1)[1]
                                    if value >= 60 and value < 70:
                                        if sValueNew.count('_Run') == 0:
                                            sValueNew = "shine_"+sValueNew
                                        else:
                                            sValueNew = "shine_"+sValueNew.split('_', 1)[1]
                                    if value >= 70:
                                        if sValueNew.count('_Run') == 0:
                                            sValueNew = "dry_"+sValueNew
                                        else:
                                            sValueNew = "dry_"+sValueNew.split('_', 1)[1]
                                #if self.selectedprogram == "Auto2":
                                #if self.selectedprogram == "Intensiv70":
                                if Devices[1].sValue != sValueNew:
                                    Devices[1].Update(nValue=Devices[1].nValue,sValue=sValueNew)
                            if key == "BSH.Common.Status.OperationState":
                                status = value.rpartition(".")[2]
                                Domoticz.Debug("status: " + status)
                                if Devices[1].sValue != status:
                                   Devices[1].Update(nValue=0,sValue=status)
    except HTTPError as httperror:
        Domoticz.Error(httperror.response.text)
    except Exception as e:
        Domoticz.Error(traceback.format_exc())

    return

"""
Method for device authorization and getting a token

Parameters
----------
self : BasePlugin
    for getting plugin variables
username : String
    Home-Connect username
password : String
    Home-Connect password
scope : String
    Scope for which authorization is requested

Return
------
None
"""
def connectHomeConnect(self,username,password,scope):
    #'Request authorization to access home appliance" and "Return device code, user code, verification uri, ..."
    url_authorization = BASEURL + "/security/oauth/device_authorization"
    scope = "IdentifyAppliance " + scope
    data_authorization = {"client_id": CLIENT_ID, "scope": scope}
    response_authorization = requests.post(url_authorization,data_authorization,HEADER_URLENCODED)
    Domoticz.Debug(response_authorization.text)
    json_data_authorization = json.loads(response_authorization.text)
    device_code = ""
    verification_uri_complete = ""
    user_code = ""
    for key, value in json_data_authorization.items():
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

    #Enter user code, log in and authorize access
    authorized = False
    if(device_code != "") and (verification_uri_complete != "") and (user_code != ""):
        session = requests.Session()

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
        response_tokenrequest = requests.post(url_tokenrequest,payload_tokenrequest, HEADER_URLENCODED)
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
        Domoticz.Log("Device \"" + device_code + "\" has token: " + self.access_token)
    else:
        Domoticz.Error("Device \"" + device_code + "\" is not authorized by Home_Connect.")

    return
