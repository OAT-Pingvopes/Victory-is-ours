import socket

f = open('data/cfg.txt', mode='r').readlines()[0].split()[2]
nickname = f[1:-1]
sock = socket.socket()
host = '26.15.82.197'
port = 5050
sock.connect((host, port))
while True:
    data = sock.recv(10240)
    sock.send()