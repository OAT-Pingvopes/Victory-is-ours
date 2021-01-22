import socket

f = open('data/cfg.txt', mode='r').readlines()[0].split()[2]
nickname = f[1:-1]
sock = socket.socket()
host = '192.168.17.232'
port = 5050
sock.connect((host, port))
print(sock)
while True:
    data = sock.recv(10240)
    print(data.decode('utf-8'))