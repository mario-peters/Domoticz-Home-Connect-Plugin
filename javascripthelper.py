#import Domoticz
def inplace_change(filename, old_string, new_string):
    #Domoticz.Debug("filename: "+filename)
    #print "filename: "+filename
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            #Domoticz.Error(old_string + " not found in " + filename)
            print old_string + " not found in " + filename
            return
    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        #Domoticz.Log("Changing "+old_string+" to "+new_string)
        print "Changing "+old_string+" to "+new_string
        s = s.replace(old_string, new_string)
        f.write(s)

def search_in_file(filename, search_string):
    with open(filename) as f:
        s = f.read()
        if search_string in s:
            print search_string + " found "
            return
