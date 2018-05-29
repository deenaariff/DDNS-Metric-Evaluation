import threading
class ResThread(threading.Thread):
    def __init__(self, conn, response):
        self.response = response
        self.conn = conn

    def run(self):
        while True:
            try:
                print('this is client response thread!')
                while(self.response is not empty):
                    d = q.get()
                    print(d)
                    self.conn.send(d)
            except Exception as e:
                print("response thread has error!" + e)
