import socket

sock = socket.socket()
host = ''
port = 5050
sock.bind((host, port))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)
f = conn.recv(1024)
print(f.decode('utf-8'))