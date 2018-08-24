# Basic Python Plugin Example
#
# Author: GizMoCuz
#
"""
<plugin key="Home-Connect" name="Home-Connect Plugin" author="Mario Peters" version="1.0.1" wikilink="https://github.com/mario-peters/Domoticz-Home-Connect-Plugin/wiki" externallink="https://github.com/mario-peters/Domoticz-Home-Connect-Plugin">
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
                <option label="Dishwasher" value="Dishwasher" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import datetime
import homeconnecthelper
#import threading
#import multiprocessing

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
        Domoticz.Heartbeat(30)
        homeconnecthelper.connectHomeConnect(self,Parameters["Username"],Parameters["Password"],Parameters["Mode1"])
        self.enabled = True
        #Create devices
        if len(Devices) == 0:
            Domoticz.Log("Create devices")
            Domoticz.Device(Name="Dishwasher-Monitor", Unit=1, TypeName="Text", Used=1).Create()

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
            if homeconnecthelper.isTokenValid(self) != True:
                if homeconnecthelper.refreshToken(self) != True:
                   homeconnecthelper.connectHomeConnect(self,Parameters["Username"],Parameters["Password"],Parameters["Mode1"])

            if self.haId == "":
                homeconnecthelper.gethaId(self)
            """ 
                if self.dishwasher_thread == None:
                    #self.dishwasher_thread = threading.Thread(name="Dishwasher-thread",target=openSSEConnection(self))
                    Domoticz.Log("start dishwasher_thread")
                    jobs = []
                    self.dishwasher_thread = multiprocessing.Process(target=openSSEConnection, args=(self,))
                    jobs.append(self.dishwasher_thread)
                    self.dishwasher_thread.start()
            """
            homeconnecthelper.openSSEConnection(self,Devices)

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
