#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
host = '192.168.0.1'
port = 5050
word = ('hello').encode()
sock.connect((host, port))
sock.send(word)

while True:
    data = sock.recv(1024)
    print(data)