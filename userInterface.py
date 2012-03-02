import sys
import httplib2
from Tkinter import *
#code we wrote:
from xmlutils import *
import resource
from urllib import quote, unquote

class UserInterface:
    #root: tkinter root
    #frame: main window pane

    #home: url to GET home dir
    #cwd: url to GET current dir

    def __init__(self, tkroot, homedir, http_handle):
        self.http_handle = http_handle
        self.home = homedir
        self.cwd = self.home
        self.downloads = "./"
        self.uploads = "./"

        #set up root window stuff
        self.root = tkroot
        self.frame = Frame(self.root, width=1000, height=500)

        #build top menu bar
        menuframe = Frame(self.root)
        Button(menuframe, text="Home", command=self.go_home).grid(row=0, column=0)
        Button(menuframe, text="Refresh", command=self.refresh).grid(row=0, column=1)
        Button(menuframe, text="Close", command=self.root.destroy).grid(row=0, column=2)
        Button(menuframe, text="Log Out", command=self.logout).grid(row=0, column=3)
        menuframe.pack()
    
        # display current (Home) directory
        self.fileframe = Frame(self.root)
        self.files = Frame(self.fileframe)
        self.refresh()
        self.fileframe.pack()

        # add buttons to create folder/upload file
        bframe = Frame(self.root)
        bframe.pack()
        b = Button(bframe, text="Create Folder", 
            command=self.create_folder_dialog,
            padx=10, pady=10).grid(row=0, column=0)
        b = Button(bframe, text="Upload File", 
            command=self.upload_file_dialog,
            padx=10, pady=10).grid(row=0, column=1)

    def go_home(self):
        self.cwd = self.home
        self.refresh()

    def go_here(self, folderName):
        def g():
            self.cwd = folderName
            self.refresh()
        return g

    def make_request(self,method, body, path):
        resp, content = self.http_handle.request(path, 
                          method, body=body, 
                          headers={'content-type':'text/plain'} )
        if not resp.status == 200:
            self.error_dialog("Server error status: " + str(resp.status) +
                    "\n" + resp.reason)
        return content

    def refresh(self):
        self.display_directory(
            parseResourceList(
                self.make_request("GET","",self.cwd)))

    #display_directory :: [Resources] -> ()
    def display_directory(self, resourceList):
        self.files.destroy()
        self.files = Frame(self.fileframe)
        dirNames = []
        fileNames = []
        i = 0
        for r in resourceList:
            print r.url
            Label(self.files, text=r.name).grid(row=i, column=0)
            if r.category == "directory":
                Button(self.files, text=unichr(8658),
                        command=self.go_here(r.url + '/')).grid(row=i, column=1)
            else:
                Button(self.files, text=unichr(8659),
                        command=self.download_file(r.url)).grid(row=i, column=1)
            if not r.name == '..':
                Button(self.files, text='X', 
                        command=self.delete_resource(r.url)).grid(row=i, column=2)
            i = i + 1
        self.files.pack()

    def upload_file_dialog(self):
        top = Toplevel()
        self.popup = top
        top.title("Which File to Upload? And where to send it?")

        self.srcinput = StringVar()
        e = Entry(top, textvariable=self.srcinput)
        e.pack()
        self.srcinput.set("Name of File to Send")

        self.destinput = StringVar()
        e = Entry(top, textvariable=self.destinput)
        e.pack()
        self.destinput.set("Name of file on server")

        button = Button(top, text="Upload", command=self.upload_file)
        button.pack()

    def upload_file(self):
        src = self.srcinput.get()
        dest = self.destinput.get()
        self.popup.destroy()
        srcpath = self.uploads + src
        desturl = self.cwd + quote(dest)

        r = Resource()
        r.initFromPath(srcpath)
        if hasattr(r , 'category'):
            r.addContent(path=srcpath)
            xmlstr = buildResourceUpload(r)
            self.make_request("PUT", xmlstr, desturl)
            self.refresh()
        else:
            self.error_dialog("File name provided does not exist.")

    def error_dialog(self, message):
        top = Toplevel()
        top.title("ERROR")
        Label(top, text="\n  " + message + "  \n").pack()
        b = Button(top, text="OK", command=top.destroy)
        b.pack()

    #Create Folder
    def create_folder_dialog(self):
        top = Toplevel()
        self.popup = top
        top.title("What name should the folder have?")

        self.destinput = StringVar()
        e = Entry(top, textvariable=self.destinput)
        e.pack()
        self.destinput.set("Name of New Folder")

        button = Button(top, text="Create", command=self.create_folder)
        button.pack()

    def create_folder(self):
        r = Resource()
        r.name = self.destinput.get()
        self.popup.destroy()
        r.category = 'directory'
        xmlstr = buildResourceUpload(r)
        self.make_request("PUT", xmlstr,self.cwd + quote(r.name))
        self.refresh()

    def download_file(self, name):
        def d():
            r = parseResourceDownload(self.make_request("GET","",name))
            r.putContent(self.downloads + r.name)
        return d

    def delete_resource(self, name):
        def d():
            self.make_request("DELETE","", name)
            self.refresh()
        return d
    
    def logout(self):
        self.root.destroy()
        self.root = Tk()
        login_dialogue(self.root) 
        self.root.mainloop()

def login_dialogue(root):
    top = Toplevel()
    top.title("Login:")

    username = StringVar()
    e = Entry(top, textvariable=username)
    e.pack()
    username.set("sampleuser")

    passwd = StringVar()
    e = Entry(top, textvariable=passwd)
    e.pack()
    passwd.set("samplepw")

    host = StringVar()
    e = Entry(top, textvariable=host)
    e.pack()
    host.set("127.0.0.1:8887")

    button = Button(top, text="Login", command=login(root, top, username, passwd, host))
    button.pack()

def login(root, top, uname, pswd, hst):
    def l():
        username = uname.get()
        passwd = pswd.get()
        host = hst.get()
        top.destroy()
        homedir = 'http://' + host + '/' + username + '/'
        print "logging into:", homedir
        h = httplib2.Http(".cache")
        h.add_credentials(username, passwd)
        app = UserInterface(root, homedir, h)
    return l

root = Tk()
login_dialogue(root)
root.mainloop()
