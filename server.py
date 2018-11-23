#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """Handle Server SIP."""
        line = self.rfile.read()
        METODO = line.split(' ')[0]
        METODOS = ['INVITE', 'BYE', 'ACK']
        IP = self.client_address[0]
        if METODO not in METODOS:
            self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n\r\n")
        elif METODO == 'INVITE':
            self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
            self.wfile.write(b"SIP/2.0 180 Ring\r\n\r\n")
            self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n" + b"\r\n")
        elif METODO == 'ACK':
            aEjecutar = 'mp32rtp -i ' + IP + ' -p 23032 < ' + sys.argv[3]
            print("Vamos a ejecutar", aEjecutar)
            os.system(aEjecutar)
            os.system('chmod 755 mp32rtp')
            print("Fin del audio")
        elif METODO == 'BYE':
            print("BYE recibido")
            self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
        else:
            print("Petición incorrecta recibida")
            self.wfile.write("SIP/2.0 400 Bad Request\r\n\r\n")


if __name__ == "__main__":
    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        sys.argv[3]
    except IndexError:
        sys.exit("Usage: python server.py IP port audio_file")
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    serv.serve_forever()
