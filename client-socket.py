import socket

nickname = 1
sock = socket.socket()
host = '26.15.82.197'
port = 5050
word = 'hello'.encode('utf-8')
sock.connect((host, port))
sock.send(word)

while True:
    data = sock.recv(10240)
    # data = data.decode('utf-8')
    # exec(data)
    print(data.decode('utf-8'))
    ans = input()
    sock.send(ans.encode('utf-8'))