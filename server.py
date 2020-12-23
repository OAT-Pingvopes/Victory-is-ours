#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

f = open('data/cfg.txt', mode='r').readlines()
f = f[0]
f = f.encode('utf-8')
sock = socket.socket()
host = ''
port = 5050
sock.bind((host, port))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.send(f)