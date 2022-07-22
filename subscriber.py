from curses import keyname
import zmq
import keyboard
from multiprocessing import Process

def choose(s):
    choice = int(input('1 - Conectar a um endereço\n2 - Inscrever em um tópico\n3 - Seguir para recebimento de mensagens'))
    print()
    if choice == 1:
        new_connect(s)
    elif choice == 2:
        new_sub(s)
    elif choice == 3:
        return
    choose(s)


def new_connect(s):
        address = input("Insert Addres[IP:PORT]: ")
        s.connect(f"tcp://{address}")

def new_sub(s):
        subs = input("Digite um tópico para se inscrever: ")
        s.setsockopt_string(zmq.SUBSCRIBE, subs)


context = zmq.Context()
s = context.socket(zmq.SUB)
s.connect("tcp://localhost:5555")
s.setsockopt_string(zmq.SUBSCRIBE, "TESTE")

choose(s)
run = 1

while run:
    msg = s.recv()
    msg = msg.decode()
    msg = msg.split(' ', 2)
    print(f'#{msg[0]}:\n{msg[1]}: {msg[2]}\n')
