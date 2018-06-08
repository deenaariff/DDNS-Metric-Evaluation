import json
import sys

fname = 'trial' + sys.argv[1] + '.txt'

data = open(fname).read()
p_data = json.loads(data)

kill_commands = 3;

l = "leader"
f = "follower"

cmd = {"cmd": "kill", "id" : "5", "val": f, "msgId": "0"};

insert_index = [50,100,150]

for index in insert_index:
	p_data = p_data[:index] + [cmd] + p_data[index:]


out = open("cmds.txt","w")
out.write(json.dumps(p_data))
out.close()

