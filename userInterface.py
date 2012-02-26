import httplib2
from xmlutils import *
from Tkinter import *
import sys
import resource

class UserInterface:
    # __init__ :: (UserInterface, main thread, [Resources]) -> ()
    def __init__(self, master, resourceList):
        self.master = master

        self.clickableDirs = Listbox(self.master)
        self.clickableDirs.pack()
        self.clickableFiles = Listbox(self.master)
        self.clickableFiles.pack()
        self.frame = Frame(self.master)

        self.display_directory(resourceList)

        self.quit = Button(self.frame, text="Close", fg="red", command=self.frame.quit)
        self.quit.pack(side=LEFT)

        self.hi_there = Button(self.frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

        self.getFile = Button(self.frame, text = "Get", command = self.say_get(resourceList))
        self.getFile.pack(side=LEFT)

        self.putFile = Button(self.frame, text = "Put", command = self.say_put)
        self.putFile.pack(side=LEFT)

        self.refreshView = Button(self.frame, text = "Refresh", command = self.refresh)
        self.refreshView.pack(side=LEFT)

        self.printSelection = Button(self.frame, text = "Print Selection", command = self.print_select)
        self.printSelection.pack(side=LEFT)

    def display_directory(self, resourceList):
        dirNames = []
        fileNames = []
        for r in resourceList:
            if r.category == 'directory':
                dirNames.append(r.name)
            else:
                fileNames.append(r.name)
        self.clickableDirs.delete(0,END)
        for dname in dirNames:
            self.clickableDirs.insert(END, dname)
        self.clickableFiles.delete(0,END)
        for fname in fileNames:
            self.clickableFiles.insert(END, fname)
        self.frame.pack()


    def say_hi(self):
        print "hi there, everyone!"

    def say_put(self):
        print "Put was called."

    def refresh(self):
        h = httplib2.Http(".cache")
        h.add_credentials('sampleuser', 'samplepw')
        resp, content = h.request("http://127.0.0.1:8887/sampleuser/", 
                          "GET", body="", 
                          headers={'content-type':'text/plain'} )
        self.display_directory(parseResourceList(content))

        print "Directory Listing Refreshed."

    def say_get(self, list):
        print "************in say get"
        resourceName = self.clickableDirs.get(ACTIVE)

        for r in list:
            if r.name == resourceName:
                if r.category == 'file':
                    r.putContent("./Downloads/" + r.name)
                    return

    def print_select(self):
        print self.clickableDirs.get(ACTIVE)




root = Tk()
h = httplib2.Http(".cache")
h.add_credentials('sampleuser', 'samplepw')

if (len(sys.argv) > 1):
    url1=sys.argv[1]
    resp, content = h.request(url1, 
                              "GET", body="", 
                              headers={'content-type':'text/plain'} )
else:
    resp, content = h.request("http://127.0.0.1:8887/sampleuser/", 
                              "GET", body="", 
                              headers={'content-type':'text/plain'} )

xmlResourceList1 = parseResourceList(content)
app = UserInterface(root, xmlResourceList1)
root.mainloop()
