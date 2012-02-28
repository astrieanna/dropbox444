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

    #user
    #password

    def __init__(self, tkroot, usrname, pswd, homedir):
        self.user = usrname
        self.password = pswd
        self.home = homedir
        self.cwd = self.home

        #set up root window stuff
        self.root = tkroot
        self.frame = Frame(self.root, width=1000, height=500)

        #build top menu bar
        menubar = Menu(self.root)
        menubar.add_command(label="Home", command=self.go_home)
        menubar.add_command(label="Refresh", command=self.refresh)
        menubar.add_command(label="Close", command=self.frame.quit)
        self.root.config(menu=menubar)

        # display current (Home) directory
        self.files = Frame(self.root)
        self.refresh()

        # add buttons to create folder/upload file
        bframe = Frame(self.root)#, height=300, width=300)
        # bframe.pack_propagate(0)
        bframe.pack()
        b = Button(bframe, text="Create Folder", 
            command=self.create_folder_dialog,
            padx=10, pady=10)
        b.pack(expand=1)
        b = Button(bframe, text="Upload File", 
            command=self.upload_file_dialog,
            padx=10, pady=10)
        b.pack(expand=1)


    #Navigation
    def go_home(self):
        print "Going home to: %s" % (self.home)

    def go_here(self, folderName):
        print "Going to: %s%s" %(self.cwd, folderName)

    def make_request(self,method, body, path):
        h = httplib2.Http(".cache")
        h.add_credentials(self.user, self.password)
        resp, content = h.request(path, 
                          method, body=body, 
                          headers={'content-type':'text/plain'} )
        return content

    #refresh :: () -> ()
    def refresh(self):
        self.display_directory(
            parseResourceList(
                self.make_request("GET","",self.cwd)))
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
        print "Download file from: %s%s" % (self.home, relpath)

    #name of resource to delete in current folder
    def delete_resource(self, name):
        print "Deleting: %s%s" % (self.cwd, name)

# Start Display
root = Tk()
app = UserInterface(root, 
    'sampleuser', 'samplepw', 'http://127.0.0.1:8887/sampleuser/')
root.mainloop()
