import socket

# Ensure Correct Number of Command Line Args
if len(sys.argv) < 3:
    raise Exception(um.NETWORK_ERR)
    exit(1)

# Set HOST and PORT INFO
HOST = sys.argv[1]
PORT = int(sys.argv[2])

# Get User for Client From Environment Variable
user = raw_input("Provide Your User Name: ")


run_client = True  # Run Client in Loop Until User Quits

while run_client:

    # New Socket Object
    s = socket.socket()

    try:

        # Connect to the host and port
        s.connect((HOST, PORT))

    # Handle any socket errors
    except socket.error as err:

        print um.SOCKET_ERROR
        print err
        exit(1)

    except KeyboardInterrupt:
        s.close()
        exit(0)

    # Close the socket connection
    s.close()