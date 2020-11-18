"""
<plugin key="Domoticz-Home-Connect-Plugin" name="Home Connect Plugin" author="Mario Peters" version="3.2.0" wikilink="https://github.com/mario-peters/Domoticz-Home-Connect-Plugin/wiki" externallink="https://github.com/mario-peters/Domoticz-Home-Connect-Plugin">
    <description>
        <h2>Home Connect domoticz plugin 3.0</h2><br/>
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Dishwasher supported</li>
            <li>Washer supported</li>
            <li>Oven supported</li>
            <li>Dryer supported</li>
            <li>Hood supported</li>
        </ul>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>Username. This is the username which you use in the Home Connect app</li>
            <li>Password. This is the password which you use in the Home Connect app</li>
            <li>Port. This is the port on which the httplistener will listen for commands from the homeconnectSSE.sh script.</li>
            <li>Scope. This is the scope of the devices according to the Home Connect API (<a href="https://developer.home-connect.com/docs/authorization/scope">API Home Connect</a>).
                <ul style="list-style-type:square">
                    <li>Dishwasher</li>
                    <li>Washer</li>
                    <li>Oven</li>
                    <li>Dryer</li>
                    <li>Hood</li>
                </ul>
            </li>
            <li>Custom icons. Option for choosing custom icons. Default is False.</li>
            <li>Client ID: Client ID of the application as you registerd in your Home Connect Developer account</li>
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
                <option label="Oven" value="Oven"/>
                <option label="Dryer" value="Dryer"/>
                <option label="Hood" value="Hood"/>
            </options>
        </param>
        <param field="Mode2" label="Custom icons" width="150px" required="false">
            <options>
                <option label="True" value="True"/>
                <option label="False" value="False" default="true"/>
            </options>
        </param>
        <param field="Mode3" label="Client ID" width="600px" required="true"/>
        <param field="Mode4" label="Device E-number" width="150px"/>
    </params>
</plugin>
"""
import Domoticz
import json
import base64
import homeconnecthelper
import datetime
import os

class BasePlugin:

    httpServerConn = None
    httpServerConns = {}
    httpClientConn = None
    clientid = ""
    haId = ""
    access_token = ""
    token_expired = datetime.datetime.now()
    refresh_token = ""
    selectedprogram = ""
    DRY_ICON = "Domoticz-Home-Connect-PluginAlt1"
    RINSE_ICON = "Domoticz-Home-Connect-PluginAlt2"
    SHINE_ICON = "Domoticz-Home-Connect-PluginAlt3"
    FINISH_ICON = "Domoticz-Home-Connect-PluginAlt4"
    CLEAN_ICON = "Domoticz-Home-Connect-PluginAlt5"
    HOMECONNECT_ICON = "Domoticz-Home-Connect-Plugin"
    DEVICE_DISHWASHER = "Dishwasher"
    DEVICE_WASHER = "Washer"
    DEVICE_OVEN = "Oven"
    DEVICE_DRYER = "Dryer"
    DEVICE_HOOD = "Hood"

    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Log("onStart called "+Parameters["Key"])
        self.clientid = Parameters["Mode3"]
        homeconnecthelper.connectHomeConnect(self,Parameters["Username"],Parameters["Password"],Parameters["Mode1"])
        self.haId = homeconnecthelper.gethaId(self,Parameters["Mode1"],Parameters["Mode4"])
        Domoticz.Log("haId: "+self.haId)
        if Parameters["Mode2"] == "True":
            loadIcons(self, Images)
        
        #Create devices
        if len(Devices) == 0:
            Domoticz.Log("Create devices")
            if self.haId != None:
                #Generic devices
                ##Operation state
                if Parameters["Mode2"] == "True":
                    #Domoticz.Device(Name="Operation state", Unit=1, TypeName="Custom", Image=Images[self.HOMECONNECT_ICON].ID).Create()
                    Domoticz.Device(Name="Operation state", Unit=1, TypeName="Text", Image=Images[self.HOMECONNECT_ICON].ID).Create()
                else:
                    Domoticz.Device(Name="Operation state", Unit=1, TypeName="Text").Create()
                
                ##Power state
                Domoticz.Device(Name="Power state", Unit=2, Type=244, Subtype=73, Switchtype=0).Create()

                ##Active program
                if Parameters["Mode2"] == "True":
                    Domoticz.Device(Name="Active program", Unit=3, TypeName="Text", Image=Images[self.HOMECONNECT_ICON].ID).Create()
                else:
                    Domoticz.Device(Name="Active program", Unit=3, TypeName="Text").Create()

                ##Program progres
                Domoticz.Device(Name="Program progress", Unit=6, TypeName="Percentage").Create()

                ##Remaining program time
                #Domoticz.Device(Name="Remaining program time", Unit=7, TypeName="Text").Create()
                if Parameters["Mode2"] == "True":
                    Domoticz.Device(Name="Remaining program time", Unit=7, TypeName="Custom", Image=Images[self.HOMECONNECT_ICON].ID).Create()
                else:
                    Domoticz.Device(Name="Remaining program time", Unit=7, TypeName="Custom").Create()

                ##Estimated time
                if Parameters["Mode2"] == "True":
                    #Domoticz.Device(Name="Estimated time", Unit=8, TypeName="Custom", Image=Images[self.HOMECONNECT_ICON].ID).Create()
                    Domoticz.Device(Name="Estimated program time", Unit=8, TypeName="Text", Image=Images[self.HOMECONNECT_ICON].ID).Create()
                else:
                    Domoticz.Device(Name="Estimated program time", Unit=8, TypeName="Text").Create()

                ##Device specific devices
                if Parameters["Mode1"] == self.DEVICE_DISHWASHER:
                    #Custom Dishwasher devices
                    if Parameters["Mode2"] == "True":
                        Domoticz.Device(Name="Current program state", Unit=4, TypeName="Text", Image=Images[self.HOMECONNECT_ICON].ID).Create()
                    else:
                        Domoticz.Device(Name="Current program state", Unit=4, TypeName="Text").Create()

                    ##Door state
                    Domoticz.Device(Name="Door state", Unit=5, Type=244, Subtype=73, Switchtype=11).Create()

                if Parameters["Mode1"] == self.DEVICE_WASHER:
                    #Customer Washer devices
                    ##Door state
                    Domoticz.Device(Name="Door state", Unit=5, Type=244, Subtype=73, Switchtype=11).Create()

                if Parameters["Mode1"] == self.DEVICE_OVEN:
                    #Custom Oven devices
                    ##Door state
                    Domoticz.Device(Name="Door state", Unit=5, Type=244, Subtype=73, Switchtype=11).Create()

                    Domoticz.Device(Name="Current cavity temperature", Unit=9, TypeName="Temperature").Create()
                if Parameters["Mode1"] == self.DEVICE_DRYER:
                    #Custom Dryer devices
                    ##Door state
                    Domoticz.Device(Name="Door state", Unit=5, Type=244, Subtype=73, Switchtype=11).Create()

                if Parameters["Mode1"] == self.DEVICE_HOOD:
                    #Custom Hood devices
                    ##Elepsed program time
                    if Parameters["Mode2"] == "True":
                        #Domoticz.Device(Name="Elapesed program time", Unit=9, TypeName="Custom", Image=Images[self.HOMECONNECT_ICON].ID).Create()
                        Domoticz.Device(Name="Elapsed program time", Unit=9, TypeName="Text", Image=Images[self.HOMECONNECT_ICON].ID).Create()
                    else:
                        Domoticz.Device(Name="Elepsed program time", Unit=9, TypeName="Text").Create()

                    ##Venting level
                    OptionsVentingLevel = {"LevelActions": "||||", "LevelNames": "FanOff|FanStage01|FanStage02|FanStage03|FanStage04|FanStage05", "LevelOffHidden": "false", "SelectorStyle": "1"}
                    Domoticz.Device(Name="Venting level", Unit=10, TypeName="Selector Switch", Options=OptionsVentingLevel).Create()

                    ##Intensive level
                    OptionsIntensiveLevel = {"LevelActions": "||||", "LevelNames": "IntensiveStageOff|IntensiveStage1|IntensiveStage2", "LevelOffHidden": "false", "SelectorStyle": "1"}
                    Domoticz.Device(Name="Intensive level", Unit=11, TypeName="Selector Switch", Options=OptionsIntensiveLevel).Create()

        operationstate = homeconnecthelper.getOperationState(self,self.haId)
        if operationstate != "" and operationstate != None:
            #Devices[1].Update(nValue=Devices[1].nValue,sValue=operationstate.rpartition(".")[2],Options={"Custom": operationstate.rpartition(".")[2]})
            Devices[1].Update(nValue=Devices[1].nValue,sValue=operationstate.rpartition(".")[2])

        powerstate = homeconnecthelper.getPowerState(self,self.haId)
        if powerstate != "" and powerstate != None:
            powerstate = powerstate.rpartition(".")[2]
            if powerstate == "On":
                Devices[2].Update(nValue=1,sValue="On")
            else:
                Devices[2].Update(nValue=0,sValue="Off")

        self.selectedprogram = homeconnecthelper.getActiveProgram(self,self.haId)
        if self.selectedprogram != "" and self.selectedprogram != None:
            self.selectedprogram = self.selectedprogram.rpartition(".")[2]
            Devices[3].Update(nValue=Devices[3].nValue,sValue=self.selectedprogram)

        doorstate = homeconnecthelper.getDoorState(self,self.haId)
        if doorstate != "" and doorstate != None:
            doorstate = doorstate.rpartition(".")[2]
            if doorstate == "Open":
                Devices[5].Update(nValue=1,sValue="Open")
            else:
                Devices[5].Update(nValue=0,sValue="Closed")

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
                    data = self.haId
                else:
                    #Domoticz.Log(a)
                    json_items = json.loads(a)
                    deviceItems = []
                    for q,w in json_items.items():
                        Domoticz.Debug(q)
                        if q == "items":
                            deviceItems = w
                    for deviceItemList in deviceItems:
                        Domoticz.Debug(str(deviceItemList))
                        deviceKey = ""
                        deviceValue = ""
                        for k in deviceItemList:
                            Domoticz.Debug(k + " —> "+str(deviceItemList[k]))
                            if k == "key":
                                deviceKey = deviceItemList[k]
                            elif k == "value":
                                deviceValue = deviceItemList[k]
                        if (deviceKey != "") and (deviceValue != ""):
                            if deviceKey == "BSH.Common.Root.SelectedProgram":
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
                                Devices[3].Update(nValue=Devices[3].nValue,sValue=deviceValue.rpartition(".")[2])
                            elif deviceKey == "BSH.Common.Option.Hood.IntensiveLevel":
                                Domoticz.Log(deviceKey+" --> "+str(deviceValue))
                                if Parameters["Mode1"] == self.DEVICE_HOOD:
                                    intensiveLevel == deviceValue.rpartition(".")[2]
                                    if intensiveLevel = "IntensiveStageOff":
                                        Devices[11].Update(nValue=0,sValue="0")
                                    elif intensiveLevel == "IntensiveStage1":
                                        Devices[11].Update(nValue=10,sValue="10")
                                    elif intensiveLevel == "IntensiveStage2":
                                        Devices[11].Update(nValue=20,sValue="20")
                            elif deviceKey == "BSH.Common.Option.Hood.VentingLevel":
                                Domoticz.Log(deviceKey+" --> "+str(deviceValue))
                                if Parameters["Mode1"] == self.DEVICE_HOOD:
                                    ventingLevel = deviceValue.rpartition(".")[2]
                                    if ventingLevel == "FanOff":
                                        Devices[10].Update(nValue=0,sValue="0")
                                    elif ventingLevel == "FanStage01":
                                        Devices[10].Update(nValue=10,sValue="10")
                                    elif ventingLevel == "FanStage02":
                                        Devices[10].Update(nValue=20,sValue="20")
                                    elif ventingLevel == "FanStage03":
                                        Devices[10].Update(nValue=30,sValue="30")
                                    elif ventingLevel == "FanStage04":
                                        Devices[10].Update(nValue=40,sValue="40")
                                    elif ventingLevel == "FanStage05":
                                        Devices[10].Update(nValue=50,sValue="50")
                            elif deviceKey == "BSH.Common.Option.ElapsedProgramTime":
                                Domoticz.Log(deviceKey+" --> "+str(deviceValue))
                                if Parameters["Mode1"] == self.DEVICE_HOOD:
                                    Devices[9].Update(nValue=0,sValue=str(deviceValue), Options={"Custom": "1;sec"})
                            elif deviceKey == "BSH.Common.Option.RemainingProgramTime":
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
                                #Devices[7].Update(nValue=deviceValue,sValue=str(deviceValue)+" sec")
                                Devices[7].Update(nValue=0,sValue=str(deviceValue), Options={"Custom": "1;sec"})
                                if deviceValue > 0:
                                    remainingTime = datetime.datetime.now() + datetime.timedelta(seconds=deviceValue)
                                    Domoticz.Debug("remainingTime: "+str(remainingTime.strftime("%H:%M")))
                                    Devices[8].Update(nValue=Devices[8].nValue,sValue=str(remainingTime.strftime("%H:%M")))
                                    #Devices[8].Update(nValue=Devices[8].nValue,sValue=str(remainingTime.hour),Options={"Custom": str(remainingTime.hour)+"; : "+str(remainingTime.strftime("%M"))})
                            elif deviceKey == "BSH.Common.Option.ProgramProgress": 
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
                                Devices[6].Update(nValue=deviceValue,sValue=str(deviceValue))
                                if Parameters["Mode1"] == self.DEVICE_DISHWASHER:
                                    if Devices[3].sValue == "PreRinse":
                                        if Parameters["Mode2"] == "True":
                                            Devices[4].Update(nValue=Devices[4].nValue,sValue="Rinse", Image=Images[self.RINSE_ICON].ID)
                                        else:
                                            Devices[4].Update(nValue=Devices[4].nValue,sValue="Rinse")
                                    #elif Devices[3].sValue == "Quick45":
                                        #TODO
                                    #elif Devices[3].sValue == "Glass48":
                                        #TODO
                                    #elif Devices[3].sValue == "Kurz40":
                                        #TODO
                                    #elif Devices[3].sValue == "NightWash":
                                        #TODO
                                    elif Devices[3].sValue == "Eco50":
                                        if deviceValue > 0 and deviceValue < 10:
                                            if Parameters["Mode2"] == "True":
                                                Devices[4].Update(nValue=Devices[4].nValue,sValue="Rinse", Image=Images[self.RINSE_ICON].ID)
                                            else:
                                                Devices[4].Update(nValue=Devices[4].nValue,sValue="Rinse")
                                        elif deviceValue >= 10 and deviceValue < 60:
                                            if Parameters["Mode2"] == "True":
                                                Devices[4].Update(nValue=Devices[4].nValue,sValue="Clean", Image=Images[self.CLEAN_ICON].ID)
                                            else:
                                                Devices[4].Update(nValue=Devices[4].nValue,sValue="Clean")
                                        elif deviceValue >= 60 and deviceValue < 70:
                                            if Parameters["Mode2"] == "True":
                                                Devices[4].Update(nValue=Devices[4].nValue,sValue="Shine", Image=Images[self.SHINE_ICON].ID)
                                            else:
                                                Devices[4].Update(nValue=Devices[4].nValue,sValue="Shine")
                                        else:
                                            if Parameters["Mode2"] == "True":
                                                Devices[4].Update(nValue=Devices[4].nValue,sValue="Dry", Image=Images[self.DRY_ICON].ID)
                                            else:
                                                Devices[4].Update(nValue=Devices[4].nValue,sValue="Dry")
                                    #elif Devices[3].sValue == "Auto2":
                                        #TODO
                                    #elif Devices[3].sValue == "Intensiv70":
                                        #TODO
                            elif deviceKey == "BSH.Common.Root.ActiveProgram":
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
                                if "." in str(deviceValue):
                                    Devices[3].Update(nValue=Devices[3].nValue,sValue=str(deviceValue).rpartition(".")[2])
                                else:
                                    Devices[3].Update(nValue=Devices[3].nValue,sValue=str(deviceValue))
                            elif deviceKey == "BSH.Common.Status.OperationState":
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
                                #Devices[1].Update(nValue=Devices[1].nValue,sValue=deviceValue.rpartition(".")[2],Options={"Custom": deviceValue.rpartition(".")[2]})
                                Devices[1].Update(nValue=Devices[1].nValue,sValue=deviceValue.rpartition(".")[2])
                            elif deviceKey == "BSH.Common.Setting.PowerState":
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
                                powerstate = deviceValue.rpartition(".")[2]
                                if powerstate == "On":
                                    Devices[2].Update(nValue=1,sValue="On")
                                else:
                                    Devices[2].Update(nValue=0,sValue="Off")
                            elif deviceKey == "BSH.Common.Status.DoorState":
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
                                doorstate = deviceValue.rpartition(".")[2]
                                if doorstate == "Open":
                                    Devices[5].Update(nValue=1,sValue="Open")
                                else:
                                    Devices[5].Update(nValue=0,sValue="Closed")
                            elif deviceKey == "BSH.Common.Event.ProgramFinished":
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
                                Devices[1].Update(nValue=Devices[1].nValue,sValue="")
                                Devices[3].Update(nValue=Devices[3].nValue,sValue="")
                                if Parameters["Mode1"] == self.DEVICE_DISHWASHER:
                                    Devices[4].Update(nValue=Devices[4].nValue,sValue="")
                                Devices[6].Update(nValue=100,sValue=str(100))
                                #Devices[7].Update(nValue=0,sValue="0 sec")
                                Devices[7].Update(nValue=0,sValue="0", Options= {"Custom": "1;sec"})
                                Devices[8].Update(nValue=0,sValue="")
                            elif deviceKey == "Cooking.Oven.Status.CurrentCavityTemperature":
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
                                if Parameters["Mode1"] == self.DEVICE_OVEN:
                                    Domoticz.Debug("Temp: "+str(deviceValue))
                                    Devices[9].Update(nValue=0,sValue=str(deviceValue))
                            else:
                                Domoticz.Log(deviceKey+" —> "+str(deviceValue))
        self.httpClientConn.Send({"Status":"200 OK", "Headers": {"Connection": "keep-alive", "Accept": "Content-Type: text/html; charset=UTF-8"}, "Data": data})

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        if Parameters["Mode1"] == self.DEVICE_DISHWASHER:
            if str(Command) == "On":
                if homeconnecthelper.setPowerState(self, self.DEVICE_DISHWASHER, str(Command)) == True:
                    Devices[Unit].Update(nValue=1,sValue="On")
            elif str(Command) == "Off":
                if homeconnecthelper.setPowerState(self, self.DEVICE_DISHWASHER, str(Command)) == True:
                    Devices[Unit].Update(nValue=1,sValue="Off")
        elif Parameters["Mode1"] == self.DEVICE_OVEN:
            if str(Command) == "On":
                if homeconnecthelper.setPowerState(self, self.DEVICE_OVEN, str(Command)) == True:
                    Devices[Unit].Update(nValue=1,sValue="On")
            elif str(Command) == "Off":
                if homeconnecthelper.setPowerState(self, self.DEVICE_OVEN, str("Standby")) == True:
                    Devices[Unit].Update(nValue=0,sValue="Off")

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

def loadIcons(self, Images):
    #Home-Connect Logo
    if self.HOMECONNECT_ICON in Images:
        Domoticz.Debug("ID: "+str(Images[self.HOMECONNECT_ICON].ID))
    else:
        Domoticz.Debug("no Home-Connect Image")
        Domoticz.Image("Home-Connect-Plugin Icons.zip").Create()

    #Dry Logo
    if self.DRY_ICON in Images:
        Domoticz.Debug("ID: "+str(Images[self.DRY_ICON].ID))
    else:
        Domoticz.Debug("no Home-Connect dry Image")
        Domoticz.Image("Home-Connect-Plugin1 Icons.zip").Create()

    #Rinse Logo
    if self.RINSE_ICON in Images:
        Domoticz.Debug("ID: "+str(Images[self.RINSE_ICON].ID))
    else:
        Domoticz.Debug("no Home-Connect rinse Image")
        Domoticz.Image("Home-Connect-Plugin2 Icons.zip").Create()

    #Shine Logo
    if self.SHINE_ICON in Images:
        Domoticz.Debug("ID: "+str(Images[self.SHINE_ICON].ID))
    else:
        Domoticz.Debug("no Home-Connect shine Image")
        Domoticz.Image("Home-Connect-Plugin3 Icons.zip").Create()

    #Finish Logo
    if self.FINISH_ICON in Images:
        Domoticz.Debug("ID: "+str(Images[self.FINISH_ICON].ID))
    else:
        Domoticz.Debug("no Home-Connect finish Image")
        Domoticz.Image("Home-Connect-Plugin4 Icons.zip").Create()

    #Clean Logo
    if self.CLEAN_ICON in Images:
        Domoticz.Debug("ID: "+str(Images[self.CLEAN_ICON].ID))
    else:
        Domoticz.Debug("no Home-Connect clean Image")
        Domoticz.Image("Home-Connect-Plugin5 Icons.zip").Create()

    Domoticz.Log(str(Images))
