#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import readline
import socket
import sys

HOST = '127.0.0.1'
PORT = 65432
PROMPT = ':: '

def help():
    print(f"Uso: {__file__}")
    print("Comandos especiales:")
    print("  exit    Salir del cliente.")
    print("  help    Mostrar esta ayuda.")

def repl():
    try:
        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Conectando al servidor en {HOST}:{PORT}...")
            client_socket.connect((HOST, PORT))
            print("Conexión establecida.")

            help()
            while True:
                try:
                    # Solicitar entrada del usuario
                    expression = input(PROMPT)
                    if expression.lower() == 'exit':
                        print("Saliendo...")
                        break
                    elif expression.lower() == 'help':
                        help()
                        continue

                    # Enviar la expresión al servidor
                    client_socket.sendall(expression.encode('utf-8'))

                    # Recibir la respuesta del servidor
                    response = client_socket.recv(1024).decode('utf-8')
                    print(f"SERVER :: --->\n{response}")

                    if expression.lower() == '..':
                        print("Saliendo...")
                        break

                except KeyboardInterrupt:
                    print("Saliendo...")
                    exit()


    except KeyboardInterrupt:
        # Manejar Ctrl+C al inicio o durante la conexión
        print("\nCliente detenido por el usuario.")
    except ConnectionRefusedError:
        print("Error: No se pudo conectar al servidor. ¿Está el servidor en ejecución?")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    repl()
