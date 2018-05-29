import threading
class ResThread(threading.Thread):
    def __init__(self, conn, response):
        super(ResThread, self).__init__()
        self.response = response
        self.conn = conn

    def run(self):
        while True:
            try:
                #print('this is client response thread!')
                while(self.response.empty() == False):
                    d = self.response.get()
                    print(d)
                break
                    #self.conn.send(d)
            except Exception as e:
                print("response thread has error!" ,e)
                break
        print("all printed")
