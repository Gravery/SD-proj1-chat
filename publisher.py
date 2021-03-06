#Programa para rodar um publisher

#Import da biblioteca zmq
import zmq

#Setup dos dados do publisher
context = zmq.Context()
s = context.socket(zmq.PUB)
port = input("Escolha uma port para hospedar(Ex: 1111): ")
s.bind("tcp://*:" + port)

#Criação do loop para envio contínuo de mensagens
run = 1
while run:
    #Input das mensagens no formato especificado
    msg = input("Formato da mensagem: [TOPICO] [NOME] [MENSAGEM]: ")
    
    #Condição de parada do publisher
    if msg == "000":
        break
    
    #Envio gerenciado pela biblioteca para todos inscritos
    s.send_string(msg)