import threading
import time
import config

class ResThread(threading.Thread):
    def __init__(self, response):
        super(ResThread, self).__init__()
        self.response = response

    def run(self):
        while True:
            try:
                
                while(self.response.empty() == False):
                    print('this is client response thread!')
                    time.sleep(2)
                    d = self.response.get()
                    print(d)
                    config.client.send(d)
                    
                    #self.conn.send(d)
            except Exception as e:
                print("response thread has error!" ,e)
                break
        print("all printed")
