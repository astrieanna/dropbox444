import sys
import httplib2
from Tkinter import *
#code we wrote:
from xmlutils import *
import resource

class UserInterface:
    #root: tkinter root
    #frame: main window pane

    #home: url to GET home dir
    #cwd: url to GET current dir

    def __init__(self, tkroot, resourceList):
        #set up root window stuff
        self.root = tkroot
        self.frame = Frame(self.root)

        #build top menu bar
        menubar = Menu(self.root)
        menubar.add_command(label="Home", command=self.go_home)
        menubar.add_command(label="Refresh", command=self.refresh)
        menubar.add_command(label="Close", command=self.frame.quit)
        self.root.config(menu=menubar)

        # display current (Home) directory
        self.display_directory(resourceList)

        # add buttons to create folder/upload file


    #Navigation
    def go_home(self):
        print "Going home to: %s" % (this.home)

    def go_here(self, folderName):
        print "Going to: %s%s" %(this.cwd, folderName)

    #refresh :: () -> ()
    def refresh(self):
        h = httplib2.Http(".cache")
        h.add_credentials('sampleuser', 'samplepw')
        resp, content = h.request("http://127.0.0.1:8887/sampleuser/", 
                          "GET", body="", 
                          headers={'content-type':'text/plain'} )
        self.display_directory(parseResourceList(content))
        print "Directory Listing Refreshed."

    #display_directory :: [Resources] -> ()
    def display_directory(self, resourceList):
        dirNames = []
        fileNames = []
        for r in resourceList:
            if r.category == 'directory':
                dirNames.append(r.name)
            else:
                fileNames.append(r.name)
        #actually show the files/dirs...

    #Upload: reldest is relative to self.cwd
    def upload_file_dialog(self):
        print "User, which file would you like to upload?"
    def upload_file(self, src, reldest):
        print "actually upload from: %s to: %s%s" % (src, self.cwd, reldest)

    #Create Folder
    def create_folder_dialog(self):
        print "And what would you like the folder to be named?"
    def create_folder(self, name):
        print "Creating new folder at: %s%s" % (self.cwd, name)

    #Downloading: relpath should be relative to the home dir
    #download_file :: String -> ()
    def download_file(self, relpath):
        print "Download file from: %s%s" % (this.home, relpath)

    #name of resource to delete in current folder
    def delete_resource(self, name):
        print "Deleting: %s%s" % (self.cwd, name)

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
