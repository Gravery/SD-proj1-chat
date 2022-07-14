
#classe para manuseio das mensagens enviadas em seus devidos tópicos
class Linda:
    def __init__(self):
        self.tupleSpace = {}
        self.inscritos = {}

    #faz a organização da mensagem enviada em seu devido tópico juntamente com o autor
    def enviar(self, tuple, author, content):
        if self.tupleSpace.get(tuple):
            self.tupleSpace[tuple].append({"autor":author, "mensagem":content})
        else:
            self.tupleSpace[tuple] = []
            self.inscritos[tuple] = []
            self.tupleSpace[tuple].append({"autor":author, "mensagem":content})
        print(self.tupleSpace)

    #realiza inscrição em um tópico
    def subscribe(self, topic, usuario):
        if self.inscritos.get(topic):
            self.inscritos[topic].append(usuario)
        else:
            return "Tópico inexistente"

    #realiza a leitura de todas mensagens enviadas em um tópico
    def ler(self, topic):
        pass
