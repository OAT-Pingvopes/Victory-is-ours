#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
host = 'Crazy-frog'
port = 9090
word = 'hello'.encode('utf-8')
sock.connect((host, port))
sock.send(word)

data = sock.recv(1024)

print(data.decode('utf-8'))