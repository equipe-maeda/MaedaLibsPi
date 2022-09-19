import time
import os

class File:
    def __init__(self, filename):
        self.filename = filename
        
    #This writes whatever is passed to it to the file     
    def write_file(self, passed):
        log = open(self.filename,"w") #open in append - creates if not existing, will append if it exists
        log.write(passed)
        log.close()
        
    def write_file_append(self, passed):
        log = open(self.filename,"a") #open in append - creates if not existing, will append if it exists
        log.write(passed)
        log.close()
        
    def read_file(self):
        try:
            log = open(self.filename, "r")
            ret = log.read()
            log.close()
            return ret
        except:
            print("Exception - Arquivo não existe.")
            return 0 
        
    #This returns the size of the file, or 0 if the file does not exist
    def CheckFileSize(self):
        # f is a file-like object.
        try:
            f = open(self.filename,"r") # Open read - this throws an error if file does not exist - in that case the size is 0
            f.seek(0, 2)
            size = f.tell()
            f.close()
            return size
        except:
            # if we wanted to know we could print some diagnostics here:
            #print("Exception - File does not exist?")
            return 0 
