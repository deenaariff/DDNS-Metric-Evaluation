client = None
leader = ("127.0.0.1", 8080)
ipList = [("127.0.0.1",8080),("127.0.0.1",8090),("127.0.0.1",9000)]
numServers = 3
electionTime = 0
round = 0

def log(m_type,message,ip=None):
    if m_type == 1:
        header = "[1. FROM CLIENT]:"
    elif m_type == 2:
        header = "[2. TO RAFT ("+ip+")]:"
    elif m_type == 3:
        header = "[3. FROM RAFT]:"
    elif m_type == 4:
        header = "[4. TO CLIENT]:"
    print header + " " + message
