#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import sys

HOST = '127.0.0.1'
PORT = 65432
ENCODING = 'utf-8'
PRINT_RESPONSE = True

def client(expression=''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(expression.encode(ENCODING))
        response = client_socket.recv(1024).decode(ENCODING)
        if PRINT_RESPONSE:
            print(response)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"ERROR. Requiere una expresión como argumento.")
        print(f"Uso:\n{__file__} <bool:response> <expresión>")
        sys.exit(1)
    else:
        if len(sys.argv) == 3:
            PRINT_RESPONSE = sys.argv[1].lower() in ['1', 'true', 'si']
            client(sys.argv[2])
        elif len(sys.argv) == 2:
            client(sys.argv[1])
