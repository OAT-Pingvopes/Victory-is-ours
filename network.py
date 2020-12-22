from twisted.internet import protocol, reactor


class Twist(protocol.Protocol):

    # Событие connectionMade срабатывает при соединении
    def connectionMade(self):
        print('connection success!')

    # Событие dataReceived - получение и отправление данных
    def dataReceived(self, data):
        print(bytes.decode(data, encoding='utf-8'))
        self.transport.write(str.encode('g', encoding='utf-8'))

    # Событие connectionLost срабатывает при разрыве соединения с клиентом
    def connectionLost(self, reason):
        print('Connection lost!')


# Конфигурация поведения протокола описывается в – классе Factory из twisted.internet.protocol.Factory
factory = protocol.Factory()
factory.protocol = Twist
print('wait...')
reactor.listenTCP(777, factory)
reactor.run()
