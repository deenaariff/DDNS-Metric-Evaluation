import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the Socket to localhost at a given port
try:
    s.bind(('', 0))
    print "Server Listening on Port: " + str(s.getsockname()[1])
except socket.error as err:
    print "Socket Connection Error %s" % err


# Listen for incoming clients and handle requests
while True:

    try:

        # conn is a new socket object
        conn, address = s.accept()

        payload = conn.recv(100000)

        if not payload:
            print "No data Exists"
        else:
            print payload

        result = True # TODO: placeholder

        conn.send(result)

    except KeyboardInterrupt:
        conn.close()
        break

    conn.close()