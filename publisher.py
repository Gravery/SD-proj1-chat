#Alunos:
#Guilherme Calça - RA 790759
#Pedro Lealdini do Prado Borges - RA 790894

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
    if len(msg.split(" ")) >= 3:
        s.send_string(msg)
        print("\nMensagem enviada com sucesso!\n\n")
    else:
        print("\nFormato inválido, tente novamente\n\n")