import socket

sock = socket.socket()
host = '192.168.0.107'
port = 5050
sock.connect((host, port))
brd = None
f = sock.recv(10240)
exec(f.decode('utf-8'))
print(brd)