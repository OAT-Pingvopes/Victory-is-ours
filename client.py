from twisted.internet import protocol, reactor
from twisted.python.compat import raw_input

f = open('data/cfg.txt', mode='r').readlines()
nickname = (f[0].split())[2]
host = 'localhost'
port = 777

class Twist_client(protocol.Protocol):
    # Отправка сообщения с проверкой
    def sendData(self):
        data = raw_input('write message: ')
        if data:
            data = nickname + ': ' + data
            self.checker = data
            self.transport.write(str.encode(data, encoding='utf-8'))
        else:
            # transport.loseConnection() - разрыв соединения
            self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self, data):
        data = bytes.decode(data, encoding='utf-8')
        if self.checker != data:
            print(data)
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