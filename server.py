#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

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
    conn.send(data)