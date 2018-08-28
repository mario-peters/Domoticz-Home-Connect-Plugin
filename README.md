Welcome to the Domoticz-Home-Connect-Plugin wiki!

# Description
This plugin makes it possible to monitor Home Connect devices in Domoticz.

# Features
Currently the following Home Connect scopes ([API Home Connect](https://developer.home-connect.com/docs/authorization/scope)) are supported
* Dishwasher-Monitor

# Configuration
* Username is the username which you use in the Home Connect app
* Password is the password which you use in the Home Connect app
* Scope is the scope of the devices according to the Home Connect API (see Features for supported scopes)

# Installation
## Default installation
* Create a directory "Home-Connect" in the Domoticz plugins directory
* Copy "plugin.py" in newly created directory
* Set the rights and ownership of the "Home-Connect" directory and "plugin.py" file correct for the Domoticz-user
* (Re)Start Domoticz

## Synolygy
Because I'm running Domoticz on my Synology, I have to do some extra installation steps. By doing the following steps I was able to start the plugin.
* Install the Synology Python3 package
* Install the Domoticz version with python from Jadahl's website ([Jadahl](http://www.jadahl.com))
* Log-in by ssh
* cd /volum1/\@appstore/py3k/usr/local/bin
* sudo wget https://bootstrap.pypa.io/get-pip.py
* sudo ./python3.5 pip install requests
* sudo ./python3.5 pip install sseclient
* cd /volume1/\@appstore/py3k/usr/local/lib
* Create the following symbolic links: certifi, chardet, idna, requests, urllib3, wheel, sseclient.py and six.py
    * sudo ln -s /volume1/\@appstore/py3k/usr/local/lib/python3.5/site-packages/certifi certifi
    * sudo ln -s /volume1/\@appstore/py3k/usr/local/lib/python3.5/site-packages/chardet chardet
    * sudo ln -s /volume1/\@appstore/py3k/usr/local/lib/python3.5/site-packages/idna idna
    * sudo ln -s /volume1/\@appstore/py3k/usr/local/lib/python3.5/site-packages/requests requests
    * sudo ln -s /volume1/\@appstore/py3k/usr/local/lib/python3.5/site-packages/urllib3 urllib3
    * sudo ln -s /volume1/\@appstore/py3k/usr/local/lib/python3.5/site-packages/wheel wheel
    * sudo ln -s /volume1/\@appstore/py3k/usr/local/lib/python3.5/site-packages/sseclient.py sseclient.py
    * sudo ln -s /volume1/\@appstore/py3k/usr/local/lib/python3.5/site-packages/six.py six.py
* Create a directory "Home-Connect" in the Domoticz plugins directory
* Copy "plugin.py" and "homeconnecthelper.py" in newly created directory
* Set the rights and ownership of the "Home-Connect" directory and "plugin.py" and "homeconnecthelper.py" files correct for the Domoticz-user. In my case user and group 1000
    * cd /usr/local/domoticz/var/plugins
    * sudo chown -R 1000 Home-Connect
    * sudo chgrp -R 1000 Home-Connect
* (Re)start Domoticz
