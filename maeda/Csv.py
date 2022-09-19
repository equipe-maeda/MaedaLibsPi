import time
import os
from maeda.SystemFile import File

class Csv:
    def __init__(self, labels = [], directory = "data.csv"):
        self.labels = labels
        self.file = File(directory)
        self._config()
        
    def _config(self):
        data_loc = []
        if not self.file.CheckFileSize():
            for i in range(0,len(self.labels)):
                if i < len(self.labels)-1:
                    self.file.write_file_append(self.labels[i]+";")
                else:
                    self.file.write_file_append(self.labels[i]+"\n")
                    
    def load_value(self, data = []):
        for i in range(0,len(data)):
            if i < len(data)-1:
                self.file.write_file_append(data[i]+";")
            else:
                self.file.write_file_append(data[i]+"\n")
            
if __name__ == "__main__":
    test = Csv(labels = ['Data', 'canal1', 'canal2', 'canal3'])
    test.load_value(["20/8/1974", "98.0", "122.6", "5.7"])
    test.load_value(["20/8/1974", "100.0", "123.4", "5.6"])
    test.load_value(["20/8/1974", "101.8.0", "124.4", "5.8"])