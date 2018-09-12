Welcome to the Domoticz-Home-Connect-Plugin wiki!

# Description
This plugin makes it possible to monitor Home Connect devices in Domoticz.

# Features
Currently the following Home Connect scopes ([API Home Connect](https://developer.home-connect.com/docs/authorization/scope)) are supported
* Dishwasher-Monitor

# Changelog
* v.1.0.2 Plugin extended with the possibility to show the progress of the dishwashing process via images. A program contains the following progress statuses Rinse, Clean, Shine and Dry. Depending on the progress, the correct picture is shown. Siemens has copyright on the original images shown by the dishwasher's infolight. The 4 pictures will therefore have to be made by yourself. The right images can be loaded via a separate python script. Since existing Domoticz (javascript) files are modified, this has been tested on Domoticz 4.9700. There is also a picture (Home-Connect.png) added as the standard icon of the plugin.
* v.1.0.1 Small bugfixes
* v.1.0.0 Initial release

# TODO
* Progress images for programs Quick45, Glas40, Kurz60, NightWash, Auto2 and Intensiv70
* New Home Connect appliances
