#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente SIP."""

import socket
import sys

# Cliente UDP simple.
if len(sys.argv) != 3:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')

METODO = sys.argv[1]
DIRECCION = sys.argv[2].split('@')

# Dirección IP del servidor.
LOGIN = DIRECCION[0]
IP = DIRECCION[1].split(':')[0]
PORT = int(DIRECCION[1].split(':')[-1])

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

# Contenido que vamos a enviar.
LINE = METODO + ' sip:' + LOGIN + '@' + IP + ' SIP/2.0\r\n'
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
print('Enviando: ' + LINE)

# Contenido que recibimos de respuesta
data = my_socket.recv(1024)
print('Recibido -- ', data.decode('utf-8'))

if METODO == 'INVITE':
    LINE = 'ACK sip:' + LOGIN + '@' + IP + ' SIP/2.0\r\n'
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    print('Enviando: ' + LINE)

# Cerramos.
my_socket.close()
print("Fin.")
