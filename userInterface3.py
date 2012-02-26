# File: hello2.py

import httplib2
from xmlutils import *
from Tkinter import *
import sys

import resource

class UserInterface:
    
    def __init__(self, master, L):
         
        resourceList = L
        L1=[]
        L2=[]
        
        for item in L:
                L1.append(item.name)
            #else:
                #L2.append(item.name)
        
        dirList = "\n \n".join(L1)
        fileList = "\n \n".join(L2)
                    
        self.listbox1 = Listbox(master)
        self.listbox1.pack()
                    
        #self.listbox2 = Listbox(master)
        # self.listbox2.pack()
                    
        for item in L1:
            self.listbox1.insert(END, item)
        
        for item in L2:
            self.listbox2.insert(END, item)
                    
        frame = Frame(master)
        frame.pack()
        
        self.message1 = Message(master, text=("DIRECTORIES: \n" + dirList))
        self.message1.pack(side = LEFT)
        self.message2 = Message(master, text=("FILES: \n" + fileList))
        self.message2.pack(side =LEFT)
        
        self.quit1 = Button(frame, text="Close", fg="red", command=frame.quit)
        self.quit1.pack(side=LEFT)
        
        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)
        
        self.getFile = Button(frame, text = "Get", command = self.say_get(resourceList))
        self.getFile.pack(side=LEFT)
        
        self.putFile = Button(frame, text = "Put", command = self.say_put)
        self.putFile.pack(side=LEFT)
        
        self.refreshView = Button(frame, text = "Refresh", command = self.refresh)
        self.refreshView.pack(side=LEFT)

        self.printSelection = Button(frame, text = "Print Selection", command = self.print_select)
        self.printSelection.pack(side=LEFT)
    
    def say_hi(self):
        print "hi there, everyone!"
    
    def say_put(self):
        print "Put was called."
    
    def refresh(self):
        #self.message2.config(text="wat")
        #self.message2.pack(side=LEFT)
        h = httplib2.Http(".cache")
        h.add_credentials('sampleuser', 'samplepw')
        resp, content = h.request("http://127.0.0.1:8887/sampleuser/", 
                          "GET", body="", 
                          headers={'content-type':'text/plain'} )

        xmlResourceList1=parseResourceList(content)
        l=xmlResourceList1
        
        L1=[]
        L2=[]
        
        for item in l:
            if item.category == 'directory':
                L1.append(item.name)
            else:
                L2.append(item.name)
        
        dirList = "\n \n".join(L1)
        fileList = "\n \n".join(L2)
        
                    #frame = Frame(master)
                    #frame.pack()
        
        self.message1.config(text="DIRECTORIES: \n" + dirList)
        self.message1.pack(side = LEFT)
        self.message2.config(text="FILES: \n" + fileList)
        self.message2.pack(side =LEFT)
        
        print "Directory Listing Refreshed."
    
    def say_get(self, list):
        print "************in say get"
        resourceName = self.listbox1.get(ACTIVE)
        
        for r in list:
            if r.name == resourceName:
                if r.category == 'file':
                    r.putContent("./Downloads/" + r.name)
                    return
                else:
    #...update display to r as the new folder...?
    
    def print_select(self):
        print self.listbox1.get(ACTIVE)


root = Tk()

#Y=resource.getResourceList("http://ddd//Users/MatthewMorris/Desktop/CNF_Assignment_1/")
#!/usr/bin/env python

h = httplib2.Http(".cache")
h.add_credentials('sampleuser', 'samplepw')

if (len(sys.argv) > 1):
    url1=sys.argv[1]
    resp, content = h.request(url1, 
                              "GET", body="", 
                              headers={'content-type':'text/plain'} )
    
else:
    # h = httplib2.Http(".cache")
    #h.add_credentials('sampleuser', 'samplepw')
    resp, content = h.request("http://127.0.0.1:8887/sampleuser/", 
                              "GET", body="", 
                              headers={'content-type':'text/plain'} )

xmlResourceList1 = parseResourceList(content)

#isList, resp1 = parseResponse(content)

#xmlResourceList1 = resp1






#for item in Y:
#print item
#Add to distinguish between file and directory

app = UserInterface(root, xmlResourceList1)

root.mainloop()   
