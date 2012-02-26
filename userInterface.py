import httplib2
from xmlutils import *
from Tkinter import *
import sys
import resource

class UserInterface:
    # __init__ :: (UserInterface, main thread, [Resources]) -> ()
    def __init__(self, master, resourceList):
        #set up master window stuff
        self.master = master
        self.frame = Frame(self.master)

        #build top menu bar
        menubar = Menu(self.master)
        menubar.add_command(label="Home", command=self.go_home)
        menubar.add_command(label="Refresh", command=self.refresh)
        menubar.add_command(label="Close", command=self.frame.quit)
        master.config(menu=menubar)

        # display current (Home) directory
        self.display_directory(resourceList)

        # add buttons to create folder/upload file


    #Navigation
    def go_home(self):
        print "ET Phone Home!"

    #Refresh
    def refresh(self):
        h = httplib2.Http(".cache")
        h.add_credentials('sampleuser', 'samplepw')
        resp, content = h.request("http://127.0.0.1:8887/sampleuser/", 
                          "GET", body="", 
                          headers={'content-type':'text/plain'} )
        self.display_directory(parseResourceList(content))
        print "Directory Listing Refreshed."

    def display_directory(self, resourceList):
        dirNames = []
        fileNames = []
        for r in resourceList:
            if r.category == 'directory':
                dirNames.append(r.name)
            else:
                fileNames.append(r.name)
        #actually show the files/dirs...

    #Upload/Creation
    def say_put(self):
        print "Put was called."

    #Downloading
    def say_get(self):
        print "************in say get"
        resourceName = self.clickableDirs.get(ACTIVE)

        for r in list:
            if r.name == resourceName:
                if r.category == 'file':
                    r.putContent("./Downloads/" + r.name)
                    return

# Grab Home Dir
h = httplib2.Http(".cache")
h.add_credentials('sampleuser', 'samplepw')
if (len(sys.argv) > 1):
    resp, content = h.request(sys.argv[1], 
                              "GET", body="", 
                              headers={'content-type':'text/plain'} )
else:
    resp, content = h.request("http://127.0.0.1:8887/sampleuser/", 
                              "GET", body="", 
                              headers={'content-type':'text/plain'} )

# Start Display
root = Tk()
app = UserInterface(root, parseResourceList(content))
root.mainloop()
