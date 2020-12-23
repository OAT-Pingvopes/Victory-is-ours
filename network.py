from twisted.internet import protocol, reactor
from twisted.internet.protocol import ServerFactory
from twisted.python.compat import raw_input

f = open('data/cfg.txt', mode='r').readlines()
nickname = (f[0].split())[2]

class Twist(protocol.Protocol):

    def __init__(self):
        self.mb = ''

    # def sendData(self):
    #     answer = raw_input(nickname + ': ')
    #     if answer:
    #         answer = nickname + ': ' + answer
    #         # self.checker = data
    #         self.transport.write(str.encode(answer, encoding='utf-8'))

    # Событие connectionMade срабатывает при соединении
    def connectionMade(self):
        print('Connection success!')
        self.factory.clientProtocols.append(self)

    # Событие dataReceived - получение и отправление данных
    def dataReceived(self, data):
        ans = bytes.decode(data, encoding='utf-8')
        print(ans)
        self.factory.sendMessageToAllClients(ans)

    # Событие connectionLost срабатывает при разрыве соединения с клиентом
    def connectionLost(self, reason):
        print('Connection lost!')
        self.factory.clientProtocols.remove(self)
        # Конфигурация поведения протокола описывается в – классе Factory из twisted.internet.protocol.Factory


class ChatProtocolFactory(ServerFactory):
    protocol = Twist

    def __init__(self):
        self.clientProtocols = []

    def sendMessageToAllClients(self, mesg):
        for client in self.clientProtocols:
            client.transport.write(str.encode(mesg, encoding='utf-8'))


factory = ChatProtocolFactory()
reactor.listenTCP(12345, factory)
reactor.run()
