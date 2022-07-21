from curses import keyname
import zmq
import keyboard
from multiprocessing import Process


def get_key(s):
    if keyboard.read_key() == "s":
        new_connect(s)
    if keyboard.read_key() == "c":
        new_sub(s)
    

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

run = 1
p1 = Process(target=get_key(s))
p1.start()

while run:
    p1.join()
    msg = s.recv()
    print(msg)
