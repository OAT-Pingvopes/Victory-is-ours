import socket

sock = socket.socket()
host = ''
port = 5050
sock.bind((host, port))
sock.listen(1)
word = 'hello'
conn, addr = sock.accept()

print('connected:', addr)

while True:
    conn.send(word.encode('utf-8'))