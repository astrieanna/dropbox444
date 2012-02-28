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

    def __init__(self, tkroot, homedir):
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
        self.cwd = self.home
        self.refresh()

    def go_here(self, folderName):
        def g():
            print "Going to: %s%s" %(self.cwd, folderName)
        return g

    def make_request(self,method, body, path):
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
        i = 0
        for r in resourceList:
            print r.name
            label = Label(self.files, text=r.name).grid(row=i, column=0)
            if r.category == "directory":
                go = Button(self.files, text=unichr(8658),
                        command=self.go_here(r.url)).grid(row=i, column=1)
            else:
                go = Button(self.files, text=unichr(8659),
                        command=self.download_file(r.url)).grid(row=i, column=1)
            delete = Button(self.files, text='X', 
                    command=self.delete_resource(r.url)).grid(row=i, column=2)
            i = i + 1
        self.files.pack()
       # for r in resourceList:
       #     if r.category == 'directory':
       #         dirNames.append(r.name)
       #     else:
       #         fileNames.append(r.name)
        #actually show the files/dirs...

    #Upload: reldest is relative to self.cwd
    def upload_file_dialog(self):
        print "User, which file would you like to upload?"
    def upload_file(self, src, reldest):
        print "actually upload from: %s to: %s%s" % (src, self.cwd, reldest)

    #Create Folder
    def create_folder_dialog(self):
        print "And what would you like the folder to be named?"
        print "testfolder1"
        self.create_folder("testfolder1")

    def create_folder(self, name):
        r = Resource()
        r.name = name
        r.category = 'directory'
        xmlstr = buildResourceUpload(r)
        self.make_request("PUT", xmlstr,self.cwd + "/" + name)
        print "Creating new folder at: %s%s" % (self.cwd, name)
        self.refresh()

    #Downloading: relpath should be relative to the home dir
    #download_file :: String -> ()
    def download_file(self, relpath):
        def d():
            print "Download file from: %s%s" % (self.home, relpath)
        return d

    #name of resource to delete in current folder
    def delete_resource(self, name):
        def d():
            print "Deleting: %s%s" % (self.cwd, name)
        return d

# Start Display

user = 'sampleuser'
password = 'samplepw'
homedir = 'http://127.0.0.1:8887/sampleuser/'
h = httplib2.Http(".cache")
h.add_credentials(user, password)

root = Tk()
app = UserInterface(root, homedir)
root.mainloop()
