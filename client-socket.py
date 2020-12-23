import socket

nickname = 1
sock = socket.socket()
host = 'Crazy-frog'
port = 5050
word = 'hello'.encode('utf-8')
sock.connect((host, port))
sock.send(word)
#
# while True:
data = sock.recv(1024)
data = data.decode('utf-8')
exec(data)
print(nickname)