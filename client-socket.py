import socket

sock = socket.socket()
host = '26.15.82.197'
port = 5050
sock.connect((host, port))

data = sock.recv(10240)
print(data.decode('utf-8'))