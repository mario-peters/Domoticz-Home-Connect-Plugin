import sys
import os
import javascripthelper

dir_path = os.path.dirname(os.path.realpath(__file__))
filename_UtilityController = dir_path + "/../../../www/app/UtilityController.js"
filename_html5cache = dir_path + "/../../../www/html5.appcache"

filename_domoticzdevices = dir_path + "/../../../www/js/domoticzdevices.js"
tab="    "
original_domoticzdevices_Icon1=tab+tab+"if (Device.useSVGtags == true) {\n"
original_domoticzdevices_Icon1=original_domoticzdevices_Icon1+tab+tab+tab+"el = makeSVGnode('image', {\n"
original_domoticzdevices_Icon1=original_domoticzdevices_Icon1+tab+tab+tab+tab+"id: this.uniquename + \"_Icon\",\n"
original_domoticzdevices_Icon1=original_domoticzdevices_Icon1+tab+tab+tab+tab+"'class': 'DeviceIcon',\n"
original_domoticzdevices_Icon2=original_domoticzdevices_Icon1+tab+tab+tab+tab+"'xlink:href': this.image,"

#javascripthelper.search_in_file(filename_domoticzdevices,original_domoticzdevices_Icon2)
replace_domoticzdevices_Icon=tab+tab+"home_connect_img=this.image;\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+"if (this.name.includes(\"Dish\")) {\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+"if (this.status.includes(\"Finish\")) {\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+"home_connect_img = \"images/finish.gif\";\n"

replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+"} else if (this.status.includes(\"Run\")) {\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+"if (this.status.includes(\"rinse_\")) {\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+tab+"home_connect_img = \"images/rinse.gif\";\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+"} else if (this.status.includes(\"clean_\")) {\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+tab+"home_connect_img = \"images/clean.gif\";\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+"} else if (this.status.includes(\"shine_\")) {\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+tab+"home_connect_img = \"images/shine.gif\";\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+"} else if (this.status.includes(\"dry_\")) {\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+tab+"home_connect_img = \"images/dry.gif\";\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+"}\n"

replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+"} else {\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+"home_connect_img = \"images/Home-Connect.png\";\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+"}\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+"}\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+"\n"
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+original_domoticzdevices_Icon1
replace_domoticzdevices_Icon=replace_domoticzdevices_Icon+tab+tab+tab+tab+"'xlink:href': home_connect_img,"

#print replace_domoticzdevices_Icon
#javascripthelper.inplace_change(filename_domoticzdevices,original_domoticzdevices_Icon2,replace_domoticzdevices_Icon)
#javascripthelper.inplace_change(filename_domoticzdevices,replace_domoticzdevices_Icon,original_domoticzdevices_Icon2)

original_domoticzdevices_Detail1=tab+tab+tab+"gImageGroup.appendChild(makeSVGnode('image', {\n"
original_domoticzdevices_Detail2=original_domoticzdevices_Detail1+tab+tab+tab+tab+"id: \"image\", 'xlink:href': this.image, width: Device.iconSize, height: Device.iconSize, opacity: this.image_opacity,"
replace_domoticzdevices_Detail=tab+tab+tab+"detail_image = this.image;\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+"if (this.name.includes(\"Dish\")) {\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+"if (this.status.includes(\"Finish\")) {\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+"detail_image = \"images/finish.gif\";\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+"} else if (this.status.includes(\"Run\")) {\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+"if (this.status.includes(\"rinse_\")) {\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+tab+"detail_image = \"images/rinse.gif\";\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+"} else if (this.status.includes(\"clean_\")) {\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+tab+"detail_image = \"images/clean.gif\";\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+"} else if (this.status.includes(\"shine_\")) {\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+tab+"detail_image = \"images/shine.gif\";\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+"} else if (this.status.includes(\"dry_\")) {\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+tab+"detail_image = \"images/dry.gif\";\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+"}\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+"} else {\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+tab+"detail_image = \"images/Home-Connect.png\";\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+"}\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+"}\n"
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+original_domoticzdevices_Detail1
replace_domoticzdevices_Detail=replace_domoticzdevices_Detail+tab+tab+tab+tab+"id: \"image\", 'xlink:href': detail_image, width: Device.iconSize, height: Device.iconSize, opacity: this.image_opacity,"

#print replace_domoticzdevices_Detail
#javascripthelper.inplace_change(filename_domoticzdevices,original_domoticzdevices_Detail2,replace_domoticzdevices_Detail)
#javascripthelper.inplace_change(filename_domoticzdevices,replace_domoticzdevices_Detail,original_domoticzdevices_Detail2)

original_image=tab+tab+tab+tab+tab+tab+tab+tab+"xhtm += 'text48.png\" height=\"48\" width=\"48\"></td>\\n';"
default_image = "\" height=\"48\" width=\"48\"></td>\\n';\n"
replace_utilitycontroller_image = ""
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+"if (item.Name.includes(\"Dish\")) {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+"if (item.Data.includes(\"Finish\")) {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"xhtm += 'finish.gif"+default_image
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+"} else if (item.Data.includes(\"Run\")) {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"if (item.Data.startsWith(\"rinse_\")) {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"xhtm += 'rinse.gif"+default_image
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"} else if (item.Data.startsWith(\"clean_\")) {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"xhtm += 'clean.gif"+default_image
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"} else if (item.Data.startsWith(\"shine_\")) {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"xhtm += 'shine.gif"+default_image
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"} else if (item.Data.startsWith(\"dry_\")) {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"xhtm += 'dry.gif"+default_image
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"} else {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"xhtm += 'Home-Connect.png"+default_image
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"}\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+"} else {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+tab+"xhtm += 'Home-Connect.png"+default_image
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+"}\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+"} else {\n"
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+tab+"xhtm += 'text48.png"+default_image
replace_utilitycontroller_image = replace_utilitycontroller_image+tab+tab+tab+tab+tab+tab+tab+tab+"}"

if len(sys.argv) == 2:
    if sys.argv[1] == "install":
        #add dishwasher bigtext for device with type "Text" in UtilityController.js
        javascripthelper.inplace_change(filename_UtilityController, "xhtm += '</td>\\n';", "else if (item.SubType == \"Text\") {if(item.Name.includes(\"Dish\")) {if(item.Data.includes(\"Run - \")){xhtm +=item.Data.split(\"un - \")[1];}}}xhtm += '</td>\\n';")
       
        #add dishwasher images for device with type "Text" in UtilityController.js
        javascripthelper.inplace_change(filename_UtilityController,original_image,replace_utilitycontroller_image)

        #remove UtilityController from appcache
        javascripthelper.inplace_change(filename_html5cache,"app/UtilityController.js","#app/UtilityController.js")
        
        #add dishwasher images for device with type "Text" in Floorplans (domoticzdevices.js)
        javascripthelper.inplace_change(filename_domoticzdevices,original_domoticzdevices_Icon2,replace_domoticzdevices_Icon)
        javascripthelper.inplace_change(filename_domoticzdevices,original_domoticzdevices_Detail2,replace_domoticzdevices_Detail)

        #remove domoticzdevices from appcache
        javascripthelper.inplace_change(filename_html5cache,"js/domoticzdevices.js","#js/domoticzdevices.js")
    elif sys.argv[1] == "uninstall":
        #remove dishwasher bigtext for device with type "Text" in UtilityController.js
        javascripthelper.inplace_change(filename_UtilityController, "else if (item.SubType == \"Text\") {if(item.Name.includes(\"Dish\")) {if(item.Data.includes(\"Run - \")){xhtm +=item.Data.split(\"un - \")[1];}}}xhtm += '</td>\\n';", "xhtm += '</td>\\n';")

        #remove dishwasher images for device with type "Text" in UtilityController.js
        javascripthelper.inplace_change(filename_UtilityController,replace_utilitycontroller_image,original_image)

        #add UtilityController to appcache
        javascripthelper.inplace_change(filename_html5cache,"#app/UtilityController.js","app/UtilityController.js")

        #remove dishwasher images for device with type "Text" in domoticzdevices.js
        javascripthelper.inplace_change(filename_domoticzdevices,replace_domoticzdevices_Icon,original_domoticzdevices_Icon2)
        javascripthelper.inplace_change(filename_domoticzdevices,replace_domoticzdevices_Detail,original_domoticzdevices_Detail2)

        #remove domoticzdevices from appcache
        javascripthelper.inplace_change(filename_html5cache,"#js/domoticzdevices.js","js/domoticzdevices.js")
    else:
        print "Argument \""+sys.argv[0]+"\" not allowed. Only install/uninstall allowed."
else:
    print "Wrong number of arguments. Only 1 argument (install/uninstall) allowed."
