import socket

sock = socket.socket()
server = ''
port = 5050
sock.bind((server, port))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)
file = open('data/save.txt', mode='r').readlines()

conn.send(file[0].encode('utf-8'))