import time
import zmq
import linda
import threading

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")
socketsub = context.socket(zmq.SUB)
socketsub.connect("tcp://localhost:5555")
message = b''
listas = linda.Linda()

#Estrutura das mensagens:
#{comando} {tópico} {autor} {mensagem}
while message != b'000':
    #  Wait for next request from client
    split = message.split(b" ", 3)
    print(f"Received request: {message}")

    if split[0].lower() == b"enviar":
        listas.enviar(split[1], split[2], split[3])
        for inscrito in listas.inscritos:
            inscrito.send_string(f'#{split[1]}#\n{split[2]}: {split[3]}\n')
    
    elif split[0].lower() == b"subscribe":
        listas.subscribe(split[1], socket)

    #  Do some 'work'
    time.sleep(0.1)

    #  Send reply back to client
    socket.send_string(f'Mensagem enviada:{message}')