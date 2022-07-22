#Programa para rodar um subscriber

#Import da biblioteca zmq
import zmq

#Função para realizar ações de conexão, inscrição e recebimento de mensagens
def choose(s):
    choice = int(input('1 - Conectar a um endereço\n2 - Inscrever em um tópico\n3 - Seguir para recebimento de mensagens\n'))
    print()
    if choice == 1:
        new_connect(s)
    elif choice == 2:
        new_sub(s)
    elif choice == 3:
        return
    choose(s)

#Função para conectar a um novo endereço a partir do IP + port
def new_connect(s):
        address = input("Insert Addres[IP:PORT]: ")
        s.connect(f"tcp://{address}")

#Função para inscrição em um tópico gerenciado pela bilbioteca zmq
def new_sub(s):
        subs = input("Digite um tópico para se inscrever: ")
        s.setsockopt_string(zmq.SUBSCRIBE, subs)


#Inicio do programa

#Setup inicial com inscrição já realizada no tópico de TESTE
context = zmq.Context()
s = context.socket(zmq.SUB)
s.connect("tcp://localhost:5555")
s.setsockopt_string(zmq.SUBSCRIBE, "TESTE")

#Chamada da função para realizar as ações
choose(s)
run = 1

#Loop infinito para recebimento de mensagens nos tópicos inscritos de todas as conexões
while run:
    msg = s.recv()
    msg = msg.decode()
    msg = msg.split(' ', 2)
    print(f'#{msg[0]}:\n{msg[1]}: {msg[2]}\n')
