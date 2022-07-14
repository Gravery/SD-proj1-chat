import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
msg = '1'

while msg != '000':
    msg = input()
    print(f"Sending request...")
    socket.send_string(msg)

    #  Get the reply.
    message = socket.recv()
    print(f"Received reply [ {message} ]")