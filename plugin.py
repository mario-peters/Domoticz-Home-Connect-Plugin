# Basic Python Plugin Example
#
# Author: GizMoCuz
#
"""
<plugin key="Domoticz-Home-Connect-Plugin" name="Home Connect Plugin" author="Mario Peters" version="1.0.2" wikilink="https://github.com/mario-peters/Domoticz-Home-Connect-Plugin/wiki" externallink="https://github.com/mario-peters/Domoticz-Home-Connect-Plugin">
    <description>
        <h2>Home Connect domoticz plugin</h2><br/>
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Dishwasher-Monitor supported</li>
            <li>Washer-Monitor supported</li>
        </ul>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>Username is the username which you use in the Home Connect app</li>
            <li>Password is the password which you use in the Home Connect app</li>
            <li>Scope is the scope of the devices according to the Home Connect API (<a href="https://developer.home-connect.com/docs/authorization/scope">API Home Connect</a>).
                <ul style="list-style-type:square">
                    <li>Dishwasher-Monitor (only supported at this moment)</li>
                </ul>
            </li>
        </ul>
        <br/><br/>
    </description>
    <params>
        <param field="Username" label="Username" width="150px" required="true"/>
        <param field="Password" label="Password" width="150px" required="true" password="true"/>
        <param field="Port" label="Port" width="150px" required="true"/>
        <param field="Mode1" label="Scope" width="150px" required="true">
            <options>
                <option label="Dishwasher" value="Dishwasher" default="true"/>
                <option label="Washer" value="Washer"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import json
import base64
import homeconnecthelper
import datetime
import os
#import threading
#import multiprocessing

class BasePlugin:

    httpServerConn = None
    httpServerConns = {}
    httpClientConn = None
    access_token = ""
    token_expired = datetime.datetime.now()
    refresh_token = ""
    selectedprogram = ""
    DRY_ICON = "Home-ConnectAlt1"
    RINSE_ICON = "Home-ConnectAlt2"
    SHINE_ICON = "Home-ConnectAlt3"
    FINISH_ICON = "Home-ConnectAlt4"
    CLEAN_ICON = "Home-ConnectAlt5"
    HOMECONNECT_ICON = "Home-Connect"

    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Log("onStart called "+Parameters["Key"])

        #Home-Connect Logo
        if self.HOMECONNECT_ICON in Images:
            Domoticz.Debug("ID: "+str(Images[self.HOMECONNECT_ICON].ID))
        else:
            Domoticz.Debug("no Home-Connect Image")
            Domoticz.Image("Home-Connect Icons.zip").Create()
        
        #Dry Logo
        if self.DRY_ICON in Images:
            Domoticz.Debug("ID: "+str(Images[self.DRY_ICON].ID))
        else:
            Domoticz.Debug("no Home-Connect dry Image")
            Domoticz.Image("Home-Connect1 Icons.zip").Create()

        #Rinse Logo
        if self.RINSE_ICON in Images:
            Domoticz.Debug("ID: "+str(Images[self.RINSE_ICON].ID))
        else:
            Domoticz.Debug("no Home-Connect rinse Image")
            Domoticz.Image("Home-Connect2 Icons.zip").Create()

        #Shine Logo
        if self.SHINE_ICON in Images:
            Domoticz.Debug("ID: "+str(Images[self.SHINE_ICON].ID))
        else:
            Domoticz.Debug("no Home-Connect shine Image")
            Domoticz.Image("Home-Connect3 Icons.zip").Create()

        #Finish Logo
        if self.FINISH_ICON in Images:
            Domoticz.Debug("ID: "+str(Images[self.FINISH_ICON].ID))
        else:
            Domoticz.Debug("no Home-Connect finish Image")
            Domoticz.Image("Home-Connect4 Icons.zip").Create()

        #Clean Logo
        if self.CLEAN_ICON in Images:
            Domoticz.Debug("ID: "+str(Images[self.CLEAN_ICON].ID))
        else:
            Domoticz.Debug("no Home-Connect clean Image")
            Domoticz.Image("Home-Connect5 Icons.zip").Create()

        Domoticz.Log(str(Images))
        homeconnecthelper.connectHomeConnect(self,Parameters["Username"],Parameters["Password"],Parameters["Mode1"])
        haId = homeconnecthelper.gethaId(self,Parameters["Mode1"])
        Domoticz.Debug("haId: "+haId)
        self.selectedprogram = homeconnecthelper.getActiveProgram(self,haId)
        if self.selectedprogram != "":
            self.selectedprogram = self.selectedprogram.rpartition(".")[2]
        
        #Create devices
        if len(Devices) == 0:
            Domoticz.Log("Create devices")
            if haId != None:
                Domoticz.Device(Name=Parameters["Mode1"]+"-Monitor", Unit=1, TypeName="Custom", Used=1, Description=haId, Image=Images[self.HOMECONNECT_ICON].ID).Create()
                Devices[1].Update(nValue=Devices[1].nValue,sValue=Devices[1].sValue,Name=Parameters["Mode1"]+"-Monitor")

        self.httpServerConn = Domoticz.Connection(Name="Home-Connect "+Parameters["Mode1"]+" WebServer", Transport="TCP/IP", Protocol="HTTP", Port=Parameters["Port"])
        self.httpServerConn.Listen()
        Domoticz.Log("Listen on Home-Connect Webserver - Port: "+str(Parameters["Port"]))

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

        if (Status == 0):
            Domoticz.Debug("Connected successfully to "+Connection.Address+":"+Connection.Port)
        else:
            Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Connection.Address+":"+Connection.Port+" with error: "+Description)
            Domoticz.Debug(str(Connection))
        if (Connection != self.httpClientConn):
            self.httpServerConns[Connection.Name] = Connection
            self.httpClientConn = Connection
        return

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")
        
        #json_items = json.loads(str(Data))
        #for key_item, value_item in json_items.items():
        data = ""
        for key_msg, value_msg in Data.items():
            Domoticz.Debug(str(key_msg)+" --> "+str(value_msg))
            if key_msg == "Data":
                a = value_msg.decode("utf-8")
                #Domoticz.Log(a)
                if a == "access_token":
                    if homeconnecthelper.isTokenValid(self) != True:
                        if homeconnecthelper.refreshToken(self) != True:
                            homeconnecthelper.connectHomeConnect(self,Parameters["Username"],Parameters["Password"],Parameters["Mode1"])
                    data = self.access_token
                elif a.startswith("haId:") == True:
                    deviceScope = a.split(":")[1]
                    Domoticz.Debug(deviceScope)
                    for d in Devices:
                        Domoticz.Log(Devices[d].Name)
                        if Devices[d].Name.startswith(deviceScope) == True:
                            data = Devices[d].Description
                else:
                    #Domoticz.Log(a)
                    json_items = json.loads(a)
                    deviceHaId = ""
                    deviceItems = None
                    for q,w in json_items.items():
                        Domoticz.Debug(q)
                        if q == "haId":
                            deviceHaId = w
                        if q == "items":
                            deviceItems = w
                    if deviceHaId != "":
                        for d in Devices:
                            if Devices[d].Description == deviceHaId:
                                for deviceItemList in deviceItems:
                                    Domoticz.Debug(str(deviceItemList))
                                    deviceKey = ""
                                    deviceValue = ""
                                    for k in deviceItemList:
                                        Domoticz.Debug(k + " --> "+str(deviceItemList[k]))
                                        if k == "key":
                                            deviceKey = deviceItemList[k]
                                        if k == "value":
                                            deviceValue = deviceItemList[k]
                                    if (deviceKey != "") and (deviceValue != ""):
                                        if deviceKey == "BSH.Common.Root.SelectedProgram":
                                            Domoticz.Log(deviceKey+" --> " + str(deviceValue).rpartition(".")[2])
                                            self.selectedprogram = deviceValue.rpartition(".")[2]
                                        elif deviceKey == "BSH.Common.Root.ActiveProgram":
                                            Domoticz.Log(deviceKey+" --> " + str(deviceValue))
                                        elif deviceKey == "BSH.Common.Option.RemainingProgramTime":
                                            Domoticz.Log(deviceKey+" --> "+str(deviceValue))
                                            remainingTimeInSeconds = int(deviceValue)
                                            if remainingTimeInSeconds > 0:
                                                remainingTime = datetime.datetime.now() + datetime.timedelta(seconds=remainingTimeInSeconds)
                                                Domoticz.Log("remainingTime: "+str(remainingTime.strftime("%H:%M")))
                                                #sValueNew = "Run - " + remainingTime.strftime("%H:%M")
                                                #sValueNew = remainingTime.strftime("%H:%M")
                                                #Domoticz.Log(str(Devices[d].sValue) + " --> "+str(sValueNew))
                                                #if str(Devices[d].sValue) != str(sValueNew):
                                                    #Devices[d].Update(nValue=deviceValue,sValue=str(sValueNew))
                                                #Devices[d].Update(nValue=Devices[d].nValue,sValue=Devices[d].sValue,Options={"Custom": "22;:15"})
                                                Devices[d].Update(nValue=Devices[d].nValue,sValue=Devices[d].sValue,Options={"Custom": str(remainingtime.hour)+";:"+str(remainingTime.minute)})
                                        elif deviceKey == "BSH.Common.Option.ProgramProgress":
                                            Domoticz.Log(deviceKey+" --> "+str(deviceValue))
                                            if self.selectedprogram == "PreRinse":
                                                Devices[d].Update(nValue=Devices[d].nValue,sValue=Devices[d].sValue,Image=Images[self.RINSE_ICON].ID)
                                            #if self.selectedprogram == "Quick45":
                                            #if self.selectedprogram == "Glas40":
                                            #if self.selectedprogram == "Kurz40":
                                            #if self.selectedprogram == "NightWash":
                                            if self.selectedprogram == "Eco50":
                                                if deviceValue > 0 and deviceValue < 10:
                                                    Devices[d].Update(nValue=Devices[d].nValue,sValue=Devices[d].sValue,Image=Images[self.RINSE_ICON].ID)
                                                if deviceValue >= 10 and deviceValue < 60:
                                                    Devices[d].Update(nValue=Devices[d].nValue,sValue=Devices[d].sValue,Image=Images[self.CLEAN_ICON].ID)
                                                if deviceValue >= 60 and deviceValue < 70:
                                                    Devices[d].Update(nValue=Devices[d].nValue,sValue=Devices[d].sValue,Image=Images[self.SHINE_ICON].ID)
                                                if deviceValue >= 70:
                                                    Devices[d].Update(nValue=Devices[d].nValue,sValue=Devices[d].sValue,Image=Images[self.DRY_ICON].ID)
                                            #if self.selectedprogram == "Auto2":
                                            #if self.selectedprogram == "Intensiv70":
                                        elif deviceKey == "BSH.Common.Status.OperationState":
                                            status = deviceValue.rpartition(".")[2]
                                            Domoticz.Log(Devices[d].Description+" has operation state "+status)
                                            if Devices[d].sValue != status:
                                                Devices[d].Update(nValue=0,sValue=status,Image=Images[self.HOMECONNECT_ICON].ID)
                                        elif deviceKey == "BSH.Common.Setting.PowerState":
                                            Domoticz.Log(Devices[d].Description+" is turned "+deviceValue.rpartition(".")[2])
                                        else:
                                            Domoticz.Log(deviceKey+" --> "+str(deviceValue))
                #Domoticz.Log(str(base64.b64decode(str(value_msg))))
                #for msgitem in value_msg:
                    #Domoticz.Log(str(msgitem))
        
        #data = "<!doctype html><html><head></head><body><h1>Succesful GET!!!</h1></body</html>"
        self.httpClientConn.Send({"Status":"200 OK", "Headers": {"Connection": "keep-alive", "Accept": "Content-Type: text/html; charset=UTF-8"}, "Data": data})

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

        if (Connection.Name in self.httpServerConns):
            del self.httpServerConns[Connection.Name]

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

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
