import socket

sock = socket.socket()
host = '192.168.0.107'
port = 5050
sock.connect((host, port))
sock.send('123435465'.encode('utf-8'))