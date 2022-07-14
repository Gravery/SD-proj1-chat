'''import time

from random import randint
from string import ascii_uppercase as uppercase
from threading import Thread

import zmq
from zmq.devices import monitored_queue

from zhelpers import zpipe

# The subscriber thread requests messages starting with
# A and B, then reads and counts incoming messages.

def subscriber_thread():
    ctx = zmq.Context.instance()

    # Subscribe to "A" and "B"
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:6001")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"B")

    count = 0
    while count < 5:
        try:
            msg = subscriber.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
            else:
                raise
        count += 1

    print ("Subscriber received %d messages" % count)


# publisher thread
# The publisher sends random messages starting with A-J:

def publisher_thread():
    ctx = zmq.Context.instance()

    publisher = ctx.socket(zmq.PUB)
    publisher.bind("tcp://*:6000")

    while True:
        string = "%s-%05d" % (uppercase[randint(0,10)], randint(0,100000))
        try:
            publisher.send(string.encode('utf-8'))
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
            else:
                raise
        time.sleep(0.1)         # Wait for 1/10th second


# listener thread
# The listener receives all messages flowing through the proxy, on its
# pipe. Here, the pipe is a pair of ZMQ_PAIR sockets that connects
# attached child threads via inproc. In other languages your mileage may vary:

def listener_thread (pipe):

    # Print everything that arrives on pipe
    while True:
        try:
            print (pipe.recv_multipart())
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted


# main thread
# The main task starts the subscriber and publisher, and then sets
# itself up as a listening proxy. The listener runs as a child thread:

def main ():

    # Start child threads
    ctx = zmq.Context.instance()
    p_thread = Thread(target=publisher_thread)
    s_thread = Thread(target=subscriber_thread)
    p_thread.start()
    s_thread.start()

    pipe = zpipe(ctx)

    subscriber = ctx.socket(zmq.XSUB)
    subscriber.connect("tcp://localhost:6000")

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://*:6001")

    l_thread = Thread(target=listener_thread, args=(pipe[1],))
    l_thread.start()

    try:
        monitored_queue(subscriber, publisher, pipe[0], b'pub', b'sub')
    except KeyboardInterrupt:
        print ("Interrupted")

    del subscriber, publisher, pipe
    ctx.term()

if __name__ == '__main__':
    main()'''

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