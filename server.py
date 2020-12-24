import socket

f = open('data/cfg.txt', mode='r').readlines()
f = f[0]
ans = f.encode('utf-8')
sock = socket.socket()
host = ''
port = 5050
sock.bind((host, port))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    data = conn.recv(10240)
    print(data.decode('utf-8'))
    if not data:
        break
    ans = input()
    conn.send(ans.encode('utf-8'))