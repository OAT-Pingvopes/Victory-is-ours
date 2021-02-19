import socket

sock = socket.socket()
host = ''
port = 5050
sock.bind((host, port))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)
data = '7865'
conn.send(data.encode('utf-8'))