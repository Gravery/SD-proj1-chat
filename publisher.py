import zmq, time

context = zmq.Context()
s = context.socket(zmq.PUB)
s.bind("tcp://*:5555")

run = 1

while run:
    msg = input("Formato da mensagem: [TOPICO] [NOME] [MENSAGEM]: ")
    if msg == "000":
        break

    msg = msg.split(" ", 2)
    s.send_string(f'{msg[0]}: {msg[1]}: {msg[2]}')