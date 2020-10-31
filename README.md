Welcome to the Domoticz-Home-Connect-Plugin wiki!

# Description
This plugin makes it possible to monitor Home Connect devices in Domoticz.

# Features
Currently the following Home Connect scopes ([API Home Connect](https://developer.home-connect.com/docs/authorization/scope)) are supported
* Dishwasher-Monitor
* Washer-Monitor
* Oven-Monitor

# Changelog
* v.3.0.1 Small fixes + power state switch functionality (turning device on or off/standby (depending on device))
* v.3.0.0 New version of the plugin with more devices
* v.2.0.2 The Client ID of you the registered Home Connect developer account is cnow onfigurable.
* v.2.0.1 After a while I found out that Domoticz isn't handling SSE (Server Side Events) from Home Connect devices very well. For solving this problem I changed the plugin to a HTTPListener. Beside the plugin you have to run the homeconnectSSE script for every Home Connect device you've added in Domoticz.
* v.1.0.2 Plugin extended with the possibility to show the progress of the dishwashing process via images. A program contains the following progress statuses Rinse, Clean, Shine Dry and Finish. Depending on the progress, the correct picture is shown. Siemens has copyright on the original images shown by the dishwasher's infolight. Because of that I haven't commited my animated gifs (copy of infolight icons of the Dishwasher). Instead you have to make the 5 pictures by yourself. The images can be loaded via a separate python script (eyes4detail.py). If you want to use this feature, then you can find the (un)install instructions on the wiki. Since existing Domoticz (javascript) files are modified, this has been tested on Domoticz 4.9700. There is also a picture (Home-Connect.png) added as the standard icon of the plugin. Siemens has also copyright on this picture. So it also has to be created by yourself.
* v.1.0.1 Small bugfixes
* v.1.0.0 Initial release

# TODO
* Progress images for programs Quick45, Glas40, Kurz60, NightWash, Auto2 and Intensiv70
* New Home Connect appliances.
