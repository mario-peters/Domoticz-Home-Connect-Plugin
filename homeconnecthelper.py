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
    response_refresh_token.close()
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
scope : String
    Devide for wich the haId must be retrieved

Return
------
haId : Retrieved String or None
"""
def gethaId(self,scope,enumber):
    url_homeappliances = BASEURL + "/api/homeappliances"
    header = {"Accept": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer "+self.access_token}
    response_homeappliances = requests.get(url_homeappliances, headers=header)
    Domoticz.Debug(response_homeappliances.text)
    json_homeappliances = json.loads(response_homeappliances.text)
    response_homeappliances.close()
    for key_homeappliance, value_homeappliance in json_homeappliances.items():
        Domoticz.Debug(key_homeappliance + " --> " + str(value_homeappliance))
        homeappliance = value_homeappliance
        for data in homeappliance:
            items = homeappliance[data]
            for item in items:
                haId = ""
                scopeType = ""
                en = ""
                for key in item:
                    Domoticz.Debug(key + " --> " + str(item[key]))
                    if key == "haId":
                        haId = item[key]
                        #self.haId = item[key]
                        #Domoticz.Debug(self.haId)
                    if key == "type":
                        scopeType = item[key]
                    if key == "enumber":
                        en = item[key]
                if scopeType == scope or (scopeType+"-Monitor") == scope:
                    if enumber == en:
                        Domoticz.Log("Enumber: "+enumber)
                        return haId
    return None

def getActiveProgram(self,haId):
    Domoticz.Debug("getActiveProgram")
    url_getActiveProgram = BASEURL + "/api/homeappliances/" + haId + "/programs/active"
    header = {"Accept": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer " + self.access_token}
    response_getActiveProgram = requests.get(url_getActiveProgram, headers=header)
    json_items = json.loads(str(response_getActiveProgram.text))
    response_getActiveProgram.close()
    Domoticz.Debug(response_getActiveProgram.text)
    for key_item, value_item in json_items.items():
        Domoticz.Debug(str(key_item)+" --> "+str(value_item))
        for data in value_item:
            if data == "key":
                Domoticz.Debug(data+" --> "+str(value_item[data]))
                return str(value_item[data])
    return ""

def getDoorState(self,haId):
    Domoticz.Debug("getDoorState")
    url_getDoorState = BASEURL + "/api/homeappliances/" + haId + "/status/BSH.Common.Status.DoorState"
    header = {"Accept": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer " + self.access_token}
    response_getDoorState = requests.get(url_getDoorState, headers=header)
    json_items = json.loads(str(response_getDoorState.text))
    response_getDoorState.close()
    Domoticz.Debug(response_getDoorState.text)
    for key_item, value_item in json_items.items():
        Domoticz.Debug(str(key_item)+" --> "+str(value_item))
        for data in value_item:
            if data == "value":
                Domoticz.Debug(data+" --> "+str(value_item[data]))
                return str(value_item[data])

def getPowerState(self,haId):
    Domoticz.Debug("getPowerState")
    url_getPowerState = BASEURL + "/api/homeappliances/" + haId + "/settings/BSH.Common.Setting.PowerState"
    header = {"Accept": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer " + self.access_token}
    response_getPowerState = requests.get(url_getPowerState, headers=header)
    json_items = json.loads(str(response_getPowerState.text))
    response_getPowerState.close()
    Domoticz.Debug(response_getPowerState.text)
    for key_item, value_item in json_items.items():
        Domoticz.Debug(str(key_item)+" --> "+str(value_item))
        for data in value_item:
            if data == "value":
                Domoticz.Debug(data+" --> "+str(value_item[data]))
                return str(value_item[data])

def setVentingLevel(self,level):
    Domoticz.Debug("setVentingLevel")
    url_setVentingLevel = BASEURL + "/api/homeappliances/"+ self.haId + "/programs/active/options/Cooking.Common.Option.Hood.VentingLevel"
    header = {"Content-Type": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer " + self.access_token}
    data = json.dumps({
      'data': {
        'key': 'Cooking.Common.Option.Hood.VentingLevel',
        'value': 'Cooking.Hood.EnumType.Stage.'+level,
        'type': 'Cooking.Hood.EnumType.Stage',
        'constrains': {
           'allowedvalues': ['Cooking.Hood.EnumType.Stage.FanOff', 'Cooking.Hood.EnumType.Stage.FanStage01', 'Cooking.Hood.EnumType.Stage.FanStage02', 'Cooking.Hood.EnumType.Stage.FanStage03', 'Cooking.Hood.EnumType.Stage.FanStage04', 'Cooking.Hood.EnumType.Stage.FanStage05']
        }
      }
    })
    response = requests.put(url_setVentingLevel, headers=header, data=data)
    Domoticz.Log(str(response.status_code))
    if str(response.status_code) == "204":
        response.close()
        return True
    response.close()
    return False 

def setIntensiveLevel(self,level):
    Domoticz.Debug("setIntensiveLevel")
    url_setIntentsiveLevel = BASEURL + "/api/homeappliances/"+ self.haId + "/programs/active/options/Cooking.Common.Option.Hood.IntensiveLevel"
    header = {"Content-Type": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer " + self.access_token}
    data = json.dumps({
      'data': {
        'key': 'Cooking.Common.Option.Hood.IntensiveLevel',
        'value': 'Cooking.Hood.EnumType.IntensiveStage.'+level,
        'type': 'Cooking.Hood.EnumType.IntensiveStage',
        'constrains': {
           'allowedvalues': ['Cooking.Hood.EnumType.IntensiveStage.IntensiveStageOff', 'Cooking.Hood.EnumType.IntensiveStage.IntensiveStage1', 'Cooking.Hood.EnumType.IntensiveStage.IntensiveStage2']
        }
      }
    })
    response = requests.put(url_setIntensiveLevel, headers=header, data=data)
    Domoticz.Log(str(response.status_code))
    if str(response.status_code) == "204":
        response.close()
        return True
    response.close()
    return False 

def setPowerState(self,devicetype,state):
    Domoticz.Debug("setPowerState")
    url_setPowerState = BASEURL + "/api/homeappliances/" + self.haId + "/settings/BSH.Common.Setting.PowerState"
    header = {"Content-Type": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer " + self.access_token}
    data = None 
    if state == "On":
        l1 = [self.DEVICE_DISHWASHER, self.DEVICE_HOOD]
        if devicetype in l1:
            data = json.dumps({
              'data': {
                'key': 'BSH.Common.Setting.PowerState',
                'value': 'BSH.Common.EnumType.PowerState.On',
                'type': 'BSH.Common.EnumType.PowerState',
                'constraints': {
                  'allowedvalues': ['BSH.Common.EnumType.Powerstate.On', 'BSH.Common.EnumType.PowerState.Off']
                }
              }
            })
        elif devicetype == self.DEVICE_OVEN:
            data = json.dumps({
              'data': {
                'key': 'BSH.Common.Setting.PowerState',
                'value': 'BSH.Common.EnumType.PowerState.On',
                'type': 'BSH.Common.EnumType.PowerState',
                'constraints': {
                  'allowedvalues': ['BSH.Common.EnumType.Powerstate.On', 'BSH.Common.EnumType.PowerState.Standby']
                }
              }
            })
    elif state == "Off":
        data = json.dumps({
          'data': {
            'key': 'BSH.Common.Setting.PowerState',
            'value': 'BSH.Common.EnumType.PowerState.Off',
            'type': 'BSH.Common.EnumType.PowerState',
            'constraints': {
              'allowedvalues': ['BSH.Common.EnumType.Powerstate.On', 'BSH.Common.EnumType.PowerState.Off']
            }
          }
        })
    elif state == "Standby":
        data = json.dumps({
          'data': {
            'key': 'BSH.Common.Setting.PowerState',
            'value': 'BSH.Common.EnumType.PowerState.Standby',
            'type': 'BSH.Common.EnumType.PowerState',
            'constraints': {
              'allowedvalues': ['BSH.Common.EnumType.Powerstate.On', 'BSH.Common.EnumType.PowerState.Standby']
            }
          }
        })
 
    response = requests.put(url_setPowerState, headers=header, data=data)
    Domoticz.Debug(str(response.status_code))
    if str(response.status_code) == "204":
        response.close()
        return True
    response.close()
    return False

def getOperationState(self,haId):
    Domoticz.Debug("getOperationState")
    url_getOperationState = BASEURL + "/api/homeappliances/" + haId + "/status/BSH.Common.Status.OperationState"
    header = {"Accept": "application/vnd.bsh.sdk.v1+json", "Authorization": "Bearer " + self.access_token}
    response_getOperationState = requests.get(url_getOperationState, headers=header)
    json_items = json.loads(str(response_getOperationState.text))
    response_getOperationState.close()
    Domoticz.Debug(response_getOperationState.text)
    for key_item, value_item in json_items.items():
        Domoticz.Debug(str(key_item)+" --> "+str(value_item))
        for data in value_item:
            if data == "value":
                Domoticz.Debug(data+" --> "+str(value_item[data]))
                return str(value_item[data])

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
ascope : String
    Scope for which authorization is requested

Return
------
None
"""
def connectHomeConnect(self,username,password,ascope):
    #'Request authorization to access home appliance" and "Return device code, user code, verification uri, ..."
    url_authorization = BASEURL + "/security/oauth/device_authorization"
    scope = "IdentifyAppliance "+ascope+"-Monitor "+ascope+"-Settings"
    data_authorization = {"client_id": self.clientid, "scope": scope}
    response_authorization = requests.post(url_authorization,data_authorization,HEADER_URLENCODED)
    Domoticz.Debug(response_authorization.text)
    json_data_authorization = json.loads(response_authorization.text)
    response_authorization.close()
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
    Domoticz.Log("device_code: "+device_code)
    Domoticz.Log("verification_uri_complete: "+verification_uri_complete)
    Domoticz.Debug("user_code: "+user_code)

    #Enter user code, log in and authorize access
    authorized = False
    
    if(device_code != "") and (verification_uri_complete != "") and (user_code != ""):
        session = requests.Session()

        #log in part
        payload_login = {"client_id": self.clientid, "user_code": user_code, "email": username, "password": password}
        url_login = BASEURL + "/security/oauth/device_login"
        response_login = session.post(url_login, data=payload_login)
        Domoticz.Debug(response_login.text)
        sessionid = response_login.text[response_login.text.find("session_id\" value=\"")+len("session_id\" value=\""):]
        sessionid = sessionid[:sessionid.find("\"")]
        Domoticz.Log("sessionid: "+sessionid)
        response_login.close()
    
        #authorize part
        #payload_grant = {"session_id": sessionid, "client_id": self.clientid, "user_code": user_code, "email": username, "app_name": APP_NAME, "scope": scope}
        payload_grant = {"user_code": user_code, "session_id": sessionid, "input_aborted": "false", "app_name": APP_NAME, "accept_language": "nl", "client_id": self.clientid, "email": username, "scope": scope, "region": "EU", "environment": "PRD"}
        url_grant = BASEURL + "/security/oauth/device_grant"
        response_grant = session.post(url_grant, data=payload_grant)
        Domoticz.Debug("response_grant: "+response_grant.text)
        authorized = True
        response_grant.close()
    
    #Token request
    if authorized:
        Domoticz.Log("Device \"" + device_code + "\" is authorized by Home-Connect.")
        url_tokenrequest = BASEURL + "/security/oauth/token"
        payload_tokenrequest = {"grant_type": "device_code", "device_code": device_code, "client_id": self.clientid}
        response_tokenrequest = requests.post(url_tokenrequest,payload_tokenrequest, HEADER_URLENCODED)
        Domoticz.Debug("response_tokenrequest: "+response_tokenrequest.text)
        json_tokenrequest = json.loads(response_tokenrequest.text)
        response_tokenrequest.close()
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
