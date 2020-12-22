from twisted.internet import protocol, reactor
from twisted.python.compat import raw_input

nickname = 'Mr.Andron'
host = 'localhost'
port = 777

class Twist_client(protocol.Protocol):
    # Отправка сообщения с проверкой
    def sendData(self):
        data = raw_input('write message: ')
        data = nickname + ': ' + data
        if data:
            self.transport.write(str.encode(data, encoding='utf-8'))
        else:
            # transport.loseConnection() - разрыв соединения
            self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self, data):
        self.sendData()


class Twist_Factory(protocol.ClientFactory):
    protocol = Twist_client

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        reactor.stop()


factory = Twist_Factory()
reactor.connectTCP(host, port, factory)
reactor.run()