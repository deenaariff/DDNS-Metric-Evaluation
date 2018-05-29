import threading
import time
import config
from util import Utility

class ResThread(threading.Thread):
    def __init__(self, response):
        super(ResThread, self).__init__()
        self.response = response

    def run(self):
        while True:
            try:
                
                while(self.response.empty() == False):
                    #print('this is client response thread!')
                    d = self.response.get()
                    #print('d')
                    #print(d)
                    data = Utility.packData(d)
                    time.sleep(0.2)
                    config.client.send(data)

            except Exception as e:
                print("response thread has error!" ,e)
                break
        print("all printed")
